from django.forms import ModelForm
from account.models import UserProfile
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile

