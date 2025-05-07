from django.contrib import admin
from .models import Goal, Habit, Task, Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'id')
    list_filter = ('user',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'progress', 'start_date', 'end_date', 'id')
    list_filter = ('user', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ('-start_date',)
    filter_horizontal = ('categories',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'frequency', 'created_at', 'id')
    list_filter = ('user', 'frequency', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'due_date', 'goal', 'status', 'completed_at', 'id')
    list_filter = ('user', 'priority', 'status', 'due_date')
    search_fields = ('title',)
    ordering = ('status', 'completed_at')
    
    


