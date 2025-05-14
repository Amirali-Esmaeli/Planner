from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm, GoalForm, HabitForm, TaskForm, CategoryForm
from django.contrib.auth.views import LoginView
from .models import Goal, Habit, Task, Category
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
import jdatetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import HabitSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        today = timezone.now().date()
        today_str = timezone.now().date().strftime('%Y-%m-%d')

        quote = None
        try:
            response = requests.get('https://api.adviceslip.com/advice')
            if response.status_code == 200:
                data = response.json()
                quote = {
                    'content': data['slip']['advice'],
                }
        except requests.RequestException:
            quote = {'content': 'امروز خودت رو به چالش بکش'}

        selected_category_id = request.GET.get('category')
        goals = Goal.objects.filter(
            user=request.user,
            ).order_by('end_date')
        if selected_category_id:
            goals = goals.filter(categories__id=selected_category_id)
            selected_category_id = int(selected_category_id) 
        goals_paginator = Paginator(goals, 3)
        goals_page = request.GET.get('goals_page', 1)
        goals = goals_paginator.get_page(goals_page)

        habits = Habit.objects.filter(user=request.user)
        valid_habits = []
        for habit in habits:
            created_date = habit.created_at.date()
            if created_date <= today:
                if habit.frequency == 'daily':
                 valid_habits.append(habit)
                elif habit.frequency == 'weekly':
                    created_weekday = created_date.weekday()
                    if today.weekday() == created_weekday:
                        valid_habits.append(habit)
                elif habit.frequency == 'monthly':
                    created_day = created_date.day
                    if today.day == created_day:
                        valid_habits.append(habit)

        selected_goal_id = request.GET.get('goal')
        tasks = Task.objects.filter(
            user=request.user,
            due_date__gte=timezone.now().date(),
            status='pending').order_by('due_date')
        if selected_goal_id:
            tasks = tasks.filter(goal_id=selected_goal_id)
            selected_goal_id = int(selected_goal_id) 
        chart_data={
            'labels':[goal.title for goal in goals],
            'data':[goal.progress for goal in goals],
        }
        categories = Category.objects.filter(user=request.user)
        context={
            'goals': goals,
            'habits': valid_habits,
            'tasks': tasks,
            'chart_data': chart_data,
            'categories': categories,
            'today_str': today_str,
            'selected_category_id': selected_category_id,
            'selected_goal_id': selected_goal_id,
            'quote': quote,
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

@login_required
def calendar(request):
    return render(request, 'core/calendar.html')

@login_required
def calendar_events(request):
    habits = Habit.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    events = []

    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.due_date.strftime('%Y-%m-%d'),
            'color': '#007bff' if task.status == 'pending' else '#28a745',
            'extendedProps': {
                'type': 'task',
                'goal': task.goal.title,
                'priority': task.get_priority_display(),
            }
        })

    end_date = timezone.now().date() + timedelta(days=365)  
    for habit in habits:
        current_date = habit.created_at.date()
        while current_date <= end_date:
            if habit.frequency == 'daily':
                events.append({
                    'title': habit.title,
                    'start': current_date.strftime('%Y-%m-%d'),
                    'color': '#ffc107',
                    'extendedProps': {
                        'type': 'habit',
                        'frequency': habit.get_frequency_display(),
                    }
                })
                current_date += timedelta(days=1)
            elif habit.frequency == 'weekly':
                events.append({
                    'title': habit.title,
                    'start': current_date.strftime('%Y-%m-%d'),
                    'color': '#ffc107',
                    'extendedProps': {
                        'type': 'habit',
                        'frequency': habit.get_frequency_display(),
                    }
                })
                current_date += timedelta(days=7)
            elif habit.frequency == 'monthly':
                events.append({
                    'title': habit.title,
                    'start': current_date.strftime('%Y-%m-%d'),
                    'color': '#ffc107',
                    'extendedProps': {
                        'type': 'habit',
                        'frequency': habit.get_frequency_display(),
                    }
                })
                shamsi_date = jdatetime.date.fromgregorian(date=current_date)
                habit_shamsi_day = jdatetime.date.fromgregorian(date=habit.created_at.date()).day
                next_shamsi_month = shamsi_date.replace(day=1) + jdatetime.timedelta(days=32)
                try:
                    next_shamsi_month = next_shamsi_month.replace(day=habit_shamsi_day)
                except ValueError:
                    next_shamsi_month = next_shamsi_month.replace(day=30)
                current_date = next_shamsi_month.togregorian()
    
    return JsonResponse(events, safe=False)

@login_required
def history(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user)
    habit_statuses = []

    for habit in habits:
        status = 'انجام نشده'
        created_date = habit.created_at.date()
        done_dates = habit.done_dates

        if habit.frequency == 'daily':
            if created_date <= today:
                if str(today) in done_dates:
                    status = 'انجام‌شده'
        elif habit.frequency == 'weekly':
            week_start = today - timedelta(days=today.weekday())
            if created_date <= today:
                week_dates = [str(week_start + timedelta(days=i)) for i in range(7)]
                if any(date in done_dates for date in week_dates):
                    status = 'انجام‌شده'
        elif habit.frequency == 'monthly':
            month_start = today.replace(day=1)
            if created_date <= today:
                month_dates = [str(month_start + timedelta(days=i)) for i in range((today - month_start).days + 1)]
                if any(date in done_dates for date in month_dates):
                    status = 'انجام‌شده'
        habit_statuses.append({'habit': habit, 'status': status})
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    task_statuses = []
    for task in tasks:
        if task.status == 'completed':
            status = 'تکمیل‌شده'
        elif task.due_date < today and task.status == 'pending':
            status = 'منقضی‌شده'
        else:
            status = 'در حال انجام'
        task_statuses.append({'task': task, 'status': status})
    
    return render(request, 'core/history.html', {
        'habit_statuses': habit_statuses,
        'task_statuses': task_statuses,
    })

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        queryset = Habit.objects.filter(user=self.request.user)
        valid_habits = []
        for habit in queryset:
            created_date = habit.created_at.date()
            if created_date <= today:
                if habit.frequency == 'daily':
                    valid_habits.append(habit.id)
                elif habit.frequency == 'weekly':
                    created_weekday = created_date.weekday()
                    if today.weekday() == created_weekday:
                        valid_habits.append(habit.id)
                elif habit.frequency == 'monthly':
                    created_day = created_date.day
                    if today.day == created_day:
                        valid_habits.append(habit.id)
        return queryset.filter(id__in=valid_habits)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        habit = self.get_object()
        today = timezone.now().date().strftime('%Y-%m-%d')
        done_dates = habit.done_dates or []
        if today not in done_dates:
            done_dates.append(today)
            habit.done_dates = done_dates
            habit.save()
            return Response({'status': 'success', 'message': 'عادت امروز انجام شد'})
        else:
            done_dates.remove(today)
            habit.done_dates = done_dates
            habit.save()
            return Response({'status': 'success', 'message': 'عادت امروز لغو شد'})
        