"""Rule-based triage engine for symptom analysis."""
from typing import List, Dict, Any

SYMPTOM_CONDITIONS: Dict[str, List[str]] = {
    'chest_pain': ['Cardiac event', 'Angina', 'Myocardial infarction', 'Pulmonary embolism', 'Aortic dissection'],
    'shortness_of_breath': ['Pulmonary embolism', 'Asthma', 'COPD exacerbation', 'Heart failure', 'Pneumonia'],
    'severe_headache': ['Subarachnoid hemorrhage', 'Meningitis', 'Hypertensive crisis', 'Migraine'],
    'sudden_vision_loss': ['Stroke', 'Retinal detachment', 'Acute angle-closure glaucoma'],
    'slurred_speech': ['Stroke', 'Transient ischemic attack', 'Hypoglycemia'],
    'facial_drooping': ['Stroke', 'Bell palsy', 'Transient ischemic attack'],
    'arm_weakness': ['Stroke', 'Transient ischemic attack', 'Cervical radiculopathy'],
    'unconsciousness': ['Syncope', 'Cardiac arrest', 'Seizure', 'Hypoglycemia'],
    'seizure': ['Epilepsy', 'Febrile seizure', 'Brain tumor', 'Meningitis'],
    'high_fever': ['Bacterial infection', 'Sepsis', 'Meningitis', 'Severe influenza'],
    'severe_abdominal_pain': ['Appendicitis', 'Ruptured ectopic pregnancy', 'Perforated ulcer', 'Pancreatitis'],
    'rectal_bleeding': ['Colorectal cancer', 'Diverticulitis', 'Hemorrhoids', 'Inflammatory bowel disease'],
    'coughing_blood': ['Tuberculosis', 'Lung cancer', 'Pulmonary embolism', 'Bronchiectasis'],
    'severe_allergic_reaction': ['Anaphylaxis'],
    'swollen_throat': ['Anaphylaxis', 'Angioedema', 'Peritonsillar abscess'],
    'fever': ['Influenza', 'COVID-19', 'Bacterial infection', 'Urinary tract infection'],
    'cough': ['Upper respiratory infection', 'Bronchitis', 'Asthma', 'COVID-19', 'Pneumonia'],
    'fatigue': ['Anemia', 'Hypothyroidism', 'Depression', 'Diabetes', 'Chronic fatigue syndrome'],
    'sore_throat': ['Pharyngitis', 'Tonsillitis', 'Strep throat', 'Mononucleosis'],
    'runny_nose': ['Common cold', 'Allergic rhinitis', 'Sinusitis'],
    'headache': ['Tension headache', 'Migraine', 'Sinusitis', 'Hypertension'],
    'nausea': ['Gastroenteritis', 'Migraine', 'Food poisoning', 'Pregnancy'],
    'vomiting': ['Gastroenteritis', 'Food poisoning', 'Appendicitis', 'Migraine'],
    'diarrhea': ['Gastroenteritis', 'Irritable bowel syndrome', 'Colitis', 'Food poisoning'],
    'abdominal_pain': ['Gastroenteritis', 'Irritable bowel syndrome', 'Peptic ulcer', 'Gallstones'],
    'dizziness': ['Vertigo', 'Anemia', 'Hypoglycemia', 'Orthostatic hypotension', 'Labyrinthitis'],
    'blurred_vision': ['Diabetic retinopathy', 'Hypertensive retinopathy', 'Cataracts', 'Migraine aura'],
    'rash': ['Contact dermatitis', 'Eczema', 'Psoriasis', 'Drug reaction', 'Viral exanthem'],
    'itching': ['Allergic reaction', 'Eczema', 'Psoriasis', 'Scabies', 'Urticaria'],
    'joint_pain': ['Osteoarthritis', 'Rheumatoid arthritis', 'Gout', 'Lupus', 'Bursitis'],
    'swelling': ['Deep vein thrombosis', 'Edema', 'Cellulitis', 'Lymphedema', 'Injury'],
    'back_pain': ['Musculoskeletal strain', 'Herniated disc', 'Kidney stones', 'Sciatica'],
    'frequent_urination': ['Urinary tract infection', 'Diabetes', 'Overactive bladder', 'Prostatitis'],
    'burning_urination': ['Urinary tract infection', 'Sexually transmitted infection', 'Kidney stones'],
    'chest_tightness': ['Asthma', 'Angina', 'Anxiety', 'GERD', 'Costochondritis'],
    'palpitations': ['Atrial fibrillation', 'Tachycardia', 'Anxiety', 'Hyperthyroidism'],
    'weight_loss': ['Diabetes', 'Cancer', 'Hyperthyroidism', 'Inflammatory bowel disease', 'Depression'],
    'increased_thirst': ['Diabetes mellitus', 'Diabetes insipidus', 'Hyperglycemia'],
    'muscle_weakness': ['Myasthenia gravis', 'Multiple sclerosis', 'Polymyositis', 'Hypothyroidism'],
    'numbness': ['Peripheral neuropathy', 'Carpal tunnel syndrome', 'Multiple sclerosis', 'Stroke'],
    'anxiety': ['Generalized anxiety disorder', 'Panic disorder', 'Hyperthyroidism', 'PTSD'],
    'depression': ['Major depressive disorder', 'Bipolar disorder', 'Hypothyroidism', 'Anemia'],
    'memory_loss': ["Alzheimer's disease", 'Vascular dementia', 'Depression', 'Vitamin B12 deficiency'],
    'ear_pain': ['Otitis media', 'Otitis externa', 'TMJ disorder', 'Eustachian tube dysfunction'],
    'eye_redness': ['Conjunctivitis', 'Uveitis', 'Dry eye syndrome', 'Subconjunctival hemorrhage'],
    'mouth_sores': ['Aphthous ulcers', 'Herpes simplex', 'Hand foot mouth disease', 'Oral cancer'],
}

EMERGENCY_SYMPTOMS = [
    'chest_pain', 'shortness_of_breath', 'severe_headache', 'sudden_vision_loss',
    'slurred_speech', 'facial_drooping', 'arm_weakness', 'unconsciousness', 'seizure',
    'high_fever', 'severe_abdominal_pain', 'coughing_blood', 'severe_allergic_reaction',
    'swollen_throat',
]

URGENT_SYMPTOMS = [
    'rectal_bleeding', 'chest_tightness', 'palpitations', 'blurred_vision',
    'dizziness', 'fever', 'vomiting', 'severe_back_pain',
]

SOON_SYMPTOMS = [
    'cough', 'fatigue', 'sore_throat', 'nausea', 'abdominal_pain', 'rash',
    'joint_pain', 'swelling', 'frequent_urination', 'burning_urination',
    'back_pain', 'ear_pain', 'eye_redness',
]

RECOMMENDATIONS = {
    'emergency': (
        "EMERGENCY: Call 911 or go to the nearest emergency room immediately. "
        "Do not drive yourself. These symptoms may indicate a life-threatening condition."
    ),
    'urgent': (
        "URGENT: Please see a doctor today or visit an urgent care center. "
        "Your symptoms require prompt medical attention within the next few hours."
    ),
    'soon': (
        "Please schedule an appointment with your doctor within the next 24-48 hours. "
        "Monitor your symptoms closely and seek emergency care if they worsen significantly."
    ),
    'routine': (
        "Your symptoms suggest a non-urgent condition. "
        "Please schedule a routine appointment with your doctor for proper evaluation and treatment."
    ),
}


class TriageEngine:
    """Rule-based triage engine for symptom analysis."""

    def analyze(self, symptoms: List[str], severity: int = 5) -> Dict[str, Any]:
        """
        Analyze symptoms and return triage result.

        Args:
            symptoms: List of symptom identifiers
            severity: Overall symptom severity 1-10

        Returns:
            dict with urgency_level, suggested_conditions, recommendation
        """
        normalized = [s.lower().replace(' ', '_') for s in symptoms]
        urgency = self._calculate_urgency(normalized, severity)
        conditions = self._get_conditions(normalized)
        recommendation = self._get_recommendation(urgency, conditions)

        return {
            'urgency_level': urgency,
            'suggested_conditions': conditions,
            'recommendation': recommendation,
        }

    def _calculate_urgency(self, symptoms: List[str], severity: int = 5) -> str:
        """Calculate urgency level based on symptom patterns and severity."""
        # Emergency: any single emergency symptom OR severity >= 9
        if severity >= 9:
            return 'emergency'
        for symptom in symptoms:
            if symptom in EMERGENCY_SYMPTOMS:
                return 'emergency'

        # Emergency combinations: classic stroke signs
        stroke_signs = {'slurred_speech', 'facial_drooping', 'arm_weakness'}
        if len(stroke_signs.intersection(set(symptoms))) >= 2:
            return 'emergency'

        # Classic acute MI presentation: chest pain with dyspnea or nausea.
        # Per AHA/ACC guidelines, this combination warrants immediate emergency evaluation.
        if 'chest_pain' in symptoms and ('shortness_of_breath' in symptoms or 'nausea' in symptoms):
            return 'emergency'

        # Urgent: any urgent symptom OR severity >= 7 with concerning symptoms
        for symptom in symptoms:
            if symptom in URGENT_SYMPTOMS:
                return 'urgent'
        if severity >= 7:
            return 'urgent'

        # Soon: moderate symptoms
        for symptom in symptoms:
            if symptom in SOON_SYMPTOMS:
                return 'soon'
        if severity >= 5:
            return 'soon'

        return 'routine'

    def _get_conditions(self, symptoms: List[str]) -> List[str]:
        """Get list of possible conditions based on symptoms."""
        conditions: Dict[str, int] = {}

        for symptom in symptoms:
            for condition in SYMPTOM_CONDITIONS.get(symptom, []):
                conditions[condition] = conditions.get(condition, 0) + 1

        # Sort by frequency (most likely first)
        sorted_conditions = sorted(conditions.items(), key=lambda x: x[1], reverse=True)
        return [condition for condition, _ in sorted_conditions[:10]]

    def _get_recommendation(self, urgency: str, conditions: List[str]) -> str:
        """Generate a recommendation string based on urgency and conditions."""
        base_recommendation = RECOMMENDATIONS.get(urgency, RECOMMENDATIONS['routine'])

        if conditions:
            top_conditions = conditions[:3]
            conditions_text = ', '.join(top_conditions)
            base_recommendation += (
                f" Possible conditions based on your symptoms include: {conditions_text}. "
                "Note: This is not a medical diagnosis. Always consult a qualified healthcare professional."
            )

        return base_recommendation
