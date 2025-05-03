from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import SignUpForm, GoalForm, HabitForm, TaskForm
from django.contrib.auth.views import LoginView
from .models import Goal, Habit, Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        goals = Goal.objects.filter(user=request.user).order_by('-start_date')[:5]
        habits = Habit.objects.filter(user=request.user, created_at__date=timezone.now().date())
        tasks = Task.objects.filter(user=request.user, completed=False).order_by('due_date')[:5]
        chart_data={
            'labels':[goal.title for goal in goals],
            'data':[goal.progress for goal in goals],
        }
        context={
            'goals':goals,
            'habits':habits,
            'tasks':tasks,
            'chart_data':chart_data
        }
        return render(request, 'core/home.html', context)
    else:
        messages.info(request, 'برای شروع برنامه‌ریزی، وارد شوید یا ثبت‌نام کنید')
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

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(user=request.user, data=request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            form.save_m2m()
            messages.success(request, 'هدف با موفقیت ایجاد شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = GoalForm(user=request.user)
    return render(request, 'core/goal_form.html', {'form': form, 'title': 'ایجاد هدف'})

@login_required
def goal_edit(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = GoalForm(user=request.user, data=request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'هدف با موفقیت ویرایش شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = GoalForm(user=request.user, instance=goal)
    return render(request, 'core/goal_form.html', {'form': form, 'title': 'ویرایش هدف'})

@login_required
def habit_create(request):
    if request.method == "POST":
        form = HabitForm(data=request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'عادت با موفقیت ایجاد شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = HabitForm()
    return render(request, 'core/habit_form.html', {'form': form, 'title': 'ایجاد عادت'})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'وظیفه با موفقیت ایجاد شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'core/task_form.html', {'form': form, 'title': 'ایجاد وظیفه'})