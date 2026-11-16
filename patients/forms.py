from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'birth_date',
            'sex',
            'address',
            'contact_number',
        ]

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }