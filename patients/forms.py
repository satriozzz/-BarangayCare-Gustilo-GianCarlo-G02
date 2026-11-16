from django import forms
from datetime import date
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
            'contact_number'
        ]

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3})
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date and birth_date > date.today():
            raise forms.ValidationError(
                "Birth date cannot be in the future."
            )

        return birth_date