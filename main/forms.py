from django import forms
from .models import *


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = [
            'child_name', 'd_o_b', 'class_enrolled', 'previous_school',
            'fathers_name', 'fathers_contact', 'fathers_occupation', 'fathers_location',
            'mothers_name', 'mothers_contact', 'mothers_occupation', 'residential',
            'religion', 'guardian_name', 'guardian_contact', 'health_status', 
            'hospital_recommendation', 'active_clubs'
        ]
        