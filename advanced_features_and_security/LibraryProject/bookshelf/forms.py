# LibraryProject/bookshelf/forms.py
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    
    email = forms.CharField(
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }))
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        }))
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validation here
        return cleaned_data
