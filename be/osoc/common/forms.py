from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Coach
# Create your forms here.

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Coach
        fields = ('first_name', 'last_name', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Coach
        fields = ('first_name', 'last_name', 'email')