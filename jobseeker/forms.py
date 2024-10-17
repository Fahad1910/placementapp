from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import StudentPofile


class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1","password2","first_name"]


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model=StudentPofile
        exclude=("user",)
        
