from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *

# Create your forms here.

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Coach
        fields = ('first_name', 'last_name', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Coach
        fields = ('first_name', 'last_name', 'email')

class SimpleSignupForm(SignupForm):
    is_admin = forms.BooleanField(label='is admin')
    first_name = forms.CharField(label="first name")
    last_name = forms.CharField(label="last name")
    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.is_admin = self.cleaned_data['is_admin']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
