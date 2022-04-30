from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Coach

# Create your forms here.

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Coach
        fields = ('email','password',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Coach
        fields = ['email', 'password', 'is_active', 'is_admin', 'is_staff']

    def clean_password(self):
        """        
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial["password"]


class SimpleSignupForm(SignupForm):
    is_admin = forms.BooleanField(label='is admin')
    first_name = forms.CharField(label="first name")
    last_name = forms.CharField(label="last name")
    def save(self, request):
        user = super().save(request)
        user.is_admin = self.cleaned_data['is_admin']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
