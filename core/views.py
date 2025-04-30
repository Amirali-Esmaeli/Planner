from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import SignUpForm
from django.contrib.auth.views import LoginView

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌ نام با موفقیت انجام شد!')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید.')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'نام کاربری یا رمز عبور اشتباه است.')
        return super().form_invalid(form)

def custom_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('core:home')
