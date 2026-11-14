from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=[
            ('STAFF', 'Staff'),
            ('MECHANIC', 'Mechanic'),
        ],
        label='Register as'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'contact_number',
            'role'
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email address is already registered.'
            )

        return email

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already registered.')
        return username

    

    


class ProfileUpdateForm(forms.ModelForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number'
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if CustomUser.objects.filter(
            email__iexact=email
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                'This email is already being used.'
            )

        return email
