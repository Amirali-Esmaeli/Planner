from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Goal, Category, Habit, Task
from django.utils import timezone

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
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'frequency', 'done']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان عادت'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'عنوان',
            'frequency': 'فرکانس',
            'done': 'انجام شده',
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'due_date', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان وظیفه'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'عنوان',
            'priority': 'اولویت',
            'due_date': 'تاریخ سررسید',
            'categories': 'دسته‌بندی‌ها',
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(user=user)

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.now().date():
            raise forms.ValidationError('تاریخ سررسید نمی‌تواند در گذشته باشد')
        return due_date