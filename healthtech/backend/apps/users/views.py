"""User views."""
import logging
import pyotp
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    MFAEnableSerializer,
    ChangePasswordSerializer,
)

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Generate JWT access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    """Register a new user."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    'message': 'User registered successfully.',
                    'user': UserProfileSerializer(user).data,
                    'tokens': tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Authenticate user and return JWT tokens."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'detail': 'Account is disabled.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if user.is_mfa_enabled:
            # Issue a short-lived opaque MFA token (300s) to complete the second factor.
            # We store only the user's UUID (non-secret identifier) keyed by the random token.
            mfa_token = get_random_string(64)
            cache.set(f'mfa_pending_{mfa_token}', str(user.id), timeout=300)
            return Response(
                {'mfa_required': True, 'mfa_token': mfa_token},
                status=status.HTTP_200_OK,
            )

        tokens = get_tokens_for_user(user)
        return Response(
            {
                'message': 'Login successful.',
                'user': UserProfileSerializer(user).data,
                'tokens': tokens,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """Logout user by blacklisting the refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the authenticated user's profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change password for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Incorrect password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class MFASetupView(APIView):
    """Setup MFA for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return QR code URL and secret for TOTP setup."""
        user = request.user
        if not user.totp_secret:
            user.totp_secret = pyotp.random_base32()
            user.save(update_fields=['totp_secret'])

        totp = pyotp.TOTP(user.totp_secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name='HealthTech',
        )
        return Response(
            {
                'secret': user.totp_secret,
                'qr_code_url': provisioning_uri,
                'mfa_enabled': user.is_mfa_enabled,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """Verify TOTP code and enable MFA."""
        serializer = MFAEnableSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.totp_secret:
            return Response(
                {'detail': 'MFA secret not set. Call GET first.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(serializer.validated_data['totp_code'], valid_window=1):
            return Response(
                {'totp_code': 'Invalid TOTP code.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_mfa_enabled = True
        user.save(update_fields=['is_mfa_enabled'])
        return Response({'message': 'MFA enabled successfully.'}, status=status.HTTP_200_OK)


class MFAVerifyView(APIView):
    """Verify TOTP code during MFA login flow."""
    permission_classes = [AllowAny]

    def post(self, request):
        mfa_token = request.data.get('mfa_token')
        totp_code = request.data.get('totp_code')

        if not mfa_token or not totp_code:
            return Response(
                {'detail': 'mfa_token and totp_code are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = cache.get(f'mfa_pending_{mfa_token}')
        if not user_id:
            return Response(
                {'detail': 'Invalid or expired MFA token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(totp_code, valid_window=1):
            return Response(
                {'totp_code': 'Invalid TOTP code.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cache.delete(f'mfa_pending_{mfa_token}')
        tokens = get_tokens_for_user(user)
        return Response(
            {
                'message': 'MFA verified. Login successful.',
                'user': UserProfileSerializer(user).data,
                'tokens': tokens,
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):
    """Request a password reset email."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            token = get_random_string(64)
            # 15-minute window aligns with HIPAA guidance on short-lived reset links
            cache.set(f'password_reset_{token}', str(user.id), timeout=900)
            # In production, send email with reset link containing the token
            logger.info(f"Password reset token for {email}: {token}")
        except CustomUser.DoesNotExist:
            # Do not reveal whether email exists
            pass

        return Response(
            {'message': 'If the email exists, a reset link has been sent.'},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """Confirm password reset with token and new password."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        user_id = cache.get(f'password_reset_{token}')
        if not user_id:
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save(update_fields=['password'])
        cache.delete(f'password_reset_{token}')
        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
