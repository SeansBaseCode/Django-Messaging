from django import forms
from app.models import *


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeated_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["password"] != cleaned_data["repeated_password"]:
            self.add_error("repeated_password", "Passwords must match")

        return cleaned_data
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
    
    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data