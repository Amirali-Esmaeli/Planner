from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    progress = models.FloatField(default=0.0)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title
    
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50, choices=[('daily', 'روزانه'), ('weekly', 'هفتگی'), ('monthly', 'ماهانه')])
    done_dates = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    priority = models.CharField(max_length=50, choices=[('low', 'کم'), ('medium', 'متوسط'), ('high', 'زیاد')])
    status = models.CharField(max_length=20, choices=[('pending', 'در حال انجام'), ('completed', 'تکمیل‌شده')], default='pending')
    due_date = models.DateField()
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
