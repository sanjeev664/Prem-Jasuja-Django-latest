from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm 
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=gettext_lazy("Enter your email address"),
    max_length=60, required=True)
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).first():
            raise ValidationError("Entered email doest not exists.")
        return email
