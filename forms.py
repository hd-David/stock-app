from wtforms.validators import DataRequired,EqualTo, Email
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, BooleanField,PasswordField, SubmitField, EmailField, IntegerField, FloatField
from flask_wtf import FlaskForm
import model

session = model.dbconnect()
User = model.User()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], )
    email = EmailField('Email', validators=[DataRequired(), Email()], )
    cash = FloatField('Cash',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = session.query(User).filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     user = session.query(User).filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')

class LoginForm():
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')