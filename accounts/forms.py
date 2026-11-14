from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email address')

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
            'email',
            'first_name',
            'last_name',
            'contact_number',
            'role'
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if CustomUser.objects.filter(Q(email__iexact=email) | Q(username__iexact=email)).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email'):
            self.instance.username = cleaned_data['email']
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
            self.save_m2m()
        return user


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email address')

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
            Q(email__iexact=email) | Q(username__iexact=email)
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already being used.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
            self.save_m2m()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Username',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
