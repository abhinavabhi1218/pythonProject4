from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.forms import fields, widgets
from .models import User, Customer
from django.utils.translation import gettext, gettext_lazy as _

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {"username": "Username", 'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(strip=False,label=_("Password"), widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(strip=False,label=_("Old Password"), 
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(strip=False,label=_("New Password"),
     widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),
      help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(strip=False,label=_("Confirm New Password"),
     widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):     
    email = forms.EmailField( label=_("Email"),  max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))
    

class MyPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(strip=False,label=_("New Password"),
     widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),
      help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(strip=False,label=_("Confirm New Password"),
     widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'zipcode', 'state']
        widgets= {'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'})
        }