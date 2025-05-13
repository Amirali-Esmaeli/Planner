from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'core'
router = DefaultRouter()
router.register(r'habits', views.HabitViewSet, basename='habit')

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('goal/edit/<int:goal_id>/', views.goal_edit, name='goal_edit'),
    path('goal/create/', views.goal_create, name='goal_create'),
    path('habit/create/', views.habit_create, name='habit_create'),
    path('task/create/', views.task_create, name='task_create'),
    path('change-password/', views.change_password, name='change_password'),
    path('habit/edit/<int:habit_id>/', views.habit_edit, name='habit_edit'),
    path('task/edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('goal/delete/<int:goal_id>/', views.goal_delete, name='goal_delete'),
    path('habit/delete/<int:habit_id>/', views.habit_delete, name='habit_delete'),
    path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('history/', views.history, name='history'),
    path('api/', include(router.urls)),
]