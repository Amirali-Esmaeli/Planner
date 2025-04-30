from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='ایمیل',widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='نام کاربری',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']