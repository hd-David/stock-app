"""Triage serializers."""
from rest_framework import serializers
from .models import SymptomCheck
from .triage_engine import TriageEngine, SYMPTOM_CONDITIONS


class SymptomCheckSerializer(serializers.ModelSerializer):
    """Serializer for reading symptom check results."""
    urgency_display = serializers.CharField(source='get_urgency_level_display', read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)

    class Meta:
        model = SymptomCheck
        fields = [
            'id', 'patient', 'patient_name', 'symptoms', 'symptom_duration',
            'symptom_severity', 'suggested_conditions', 'urgency_level', 'urgency_display',
            'recommendation', 'additional_notes', 'created_at',
        ]
        read_only_fields = [
            'id', 'patient', 'suggested_conditions', 'urgency_level',
            'recommendation', 'created_at',
        ]


class SymptomCheckCreateSerializer(serializers.Serializer):
    """Serializer for creating a symptom check – calls triage engine."""
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        help_text="List of symptom identifiers.",
    )
    symptom_duration = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    symptom_severity = serializers.IntegerField(min_value=1, max_value=10, default=5)
    additional_notes = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_symptoms(self, value):
        known = set(SYMPTOM_CONDITIONS.keys())
        unknown = [s for s in value if s.lower().replace(' ', '_') not in known]
        if unknown:
            raise serializers.ValidationError(
                f"Unknown symptom(s): {', '.join(unknown)}. "
                f"Valid symptoms: {', '.join(sorted(known))}."
            )
        return value

    def create(self, validated_data):
        patient = validated_data.pop('patient')
        symptoms = validated_data['symptoms']
        severity = validated_data.get('symptom_severity', 5)

        engine = TriageEngine()
        result = engine.analyze(symptoms, severity)

        return SymptomCheck.objects.create(
            patient=patient,
            symptoms=symptoms,
            symptom_duration=validated_data.get('symptom_duration', ''),
            symptom_severity=severity,
            suggested_conditions=result['suggested_conditions'],
            urgency_level=result['urgency_level'],
            recommendation=result['recommendation'],
            additional_notes=validated_data.get('additional_notes', ''),
        )
