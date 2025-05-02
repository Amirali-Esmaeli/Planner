from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('goal/edit/<int:goal_id>/', views.goal_edit, name='goal_edit'),
    path('goal/create/', views.goal_create, name='goal_create'),
    path('habit/create/', views.habit_create, name='habit_create'),
    path('task/create/', views.task_create, name='task_create'),
]