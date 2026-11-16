from django import forms
from datetime import date
from .models import Patient
from .models import PatientVisit
from datetime import date


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

class PatientVisitForm(forms.ModelForm):
    class Meta:
        model = PatientVisit
        fields = ['patient', 'visit_date', 'purpose', 'notes']

        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and user.role == 'ADMIN':
            self.fields['patient'].queryset = Patient.objects.all()
        elif user and user.role == 'HEALTH_WORKER':
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)
        else:
            self.fields['patient'].queryset = Patient.objects.none()

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')

        if visit_date and visit_date > date.today():
            raise forms.ValidationError("Visit date cannot be in the future.")

        return visit_date