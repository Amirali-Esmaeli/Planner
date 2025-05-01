from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Goal, Category

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='ایمیل',widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='نام کاربری',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'progress', 'start_date', 'end_date', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان هدف'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':4, 'placeholder': 'توضیحات'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'typr': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
        }  
        labels = {
            'title': 'عنوان',
            'description': 'توضیحات',
            'progress': 'پیشرفت (%)',
            'start_date': 'تاریخ شروع',
            'end_date': 'تاریخ پایان',
            'categories': 'دسته‌بندی‌ها',
        }

        def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['categories'].queryset = Category.objects.filter(user=user)