from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm, GoalForm, HabitForm, TaskForm, CategoryForm
from django.contrib.auth.views import LoginView
from .models import Goal, Habit, Task, Category
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        goals = Goal.objects.filter(user=request.user).order_by('-start_date')[:5]
        habits = Habit.objects.filter(user=request.user, created_at__date=timezone.now().date())
        tasks = Task.objects.filter(
            user=request.user,
            due_date__gte=timezone.now().date(),
            status='pending').order_by('due_date')[:5]
        chart_data={
            'labels':[goal.title for goal in goals],
            'data':[goal.progress for goal in goals],
        }
        categories = Category.objects.filter(user=request.user)
        context={
            'goals':goals,
            'habits':habits,
            'tasks':tasks,
            'chart_data':chart_data,
            'categories':categories,
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
        form = TaskForm(user=request.user,data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'وظیفه با موفقیت ایجاد شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'core/task_form.html', {'form': form, 'title': 'ایجاد وظیفه'})

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'core/change_password.html', {'form': form})

@login_required
def habit_edit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        form = HabitForm(data=request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'عادت با موفقیت ویرایش شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'core/habit_form.html', {'form': form, 'title': 'ویرایش عادت'})

@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        habit.delete()
        messages.success(request, 'عادت با موفقیت حذف شد')
        return redirect('core:home')
    return render(request, 'core/habit_delete.html', {'habit': habit})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(user=request.user, data=request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'وظیفه با موفقیت ویرایش شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = TaskForm(user=request.user, instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'title': 'ویرایش وظیفه'})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, 'وظیفه با موفقیت حذف شد')
        return redirect('core:home')
    return render(request, 'core/task_delete.html', {'task': task})

@login_required
def goal_delete(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == "POST":
        goal.delete()
        messages.success(request, 'هدف با موفقیت حذف شد')
        return redirect('core:home')
    return render(request, 'core/goal_delete.html', {'goal': goal})
    
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'دسته‌بندی با موفقیت ایجاد شد')
            return redirect('core:home')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید')
    else:
        form = CategoryForm()
    return render(request, 'core/category_form.html', {'form': form, 'title': 'ایجاد دسته‌بندی'})

@login_required
def category_delete(request,category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    messages.success(request, 'دسته‌بندی با موفقیت حذف شد')
    return redirect('core:home')