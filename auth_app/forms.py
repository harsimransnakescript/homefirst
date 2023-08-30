from django import forms
from django.core.exceptions import ValidationError
from .models import *

class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control','id':'email','placeholder':'Enter your email'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','id':'first_name','placeholder':'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Enter your last name'}),
        }


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
