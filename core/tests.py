from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Goal, Task, Habit
from rest_framework.test import APIClient
from datetime import timedelta
import json

# Create your tests here.

class PlannerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        self.api_client = APIClient()
        self.api_client.login(username='testuser', password='testpass')

        self.category = Category.objects.create(user=self.user, name='سلامتی')
        self.goal = Goal.objects.create(
            user=self.user,
            title='کاهش وزن',
            description='کاهش ۵ کیلو',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            progress=50.0
        )
        self.goal.categories.add(self.category)
        self.task = Task.objects.create(
            user=self.user,
            title='ورزش صبح',
            goal=self.goal,
            due_date=timezone.now().date(),
            priority='high',
            status='pending'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            title='مطالعه روزانه',
            frequency='daily',
            done_dates=['2025-05-14'],
            created_at=timezone.now()
        )

    def test_category_model(self):
        self.assertEqual(str(self.category), 'سلامتی')
        self.assertEqual(self.category.user, self.user)
    
    def test_goal_model(self):
        self.assertEqual(str(self.goal), 'کاهش وزن')
        self.assertEqual(self.goal.progress, 50.0)
        self.assertIn(self.category, self.goal.categories.all())
    
    def test_task_model(self):
        self.assertEqual(str(self.task), 'ورزش صبح')
        self.assertEqual(self.task.goal, self.goal)
        self.assertEqual(self.task.priority, 'high')
        self.assertEqual(self.task.status, 'pending')

    def test_habit_model(self):
        self.assertEqual(str(self.habit), 'مطالعه روزانه')
        self.assertEqual(self.habit.frequency, 'daily')
        self.assertIn('2025-05-14', self.habit.done_dates)

    def test_home_view_authenticated(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, 'کاهش وزن')
        self.assertContains(response, 'ورزش صبح')
        self.assertContains(response, 'مطالعه روزانه')
        self.assertTrue('quote' in response.context)
        self.assertIn('content', response.context['quote'])

    def test_home_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, 'برای شروع برنامه‌ریزی، وارد شوید')

    def test_category_filter(self):
        response = self.client.get(reverse('core:home'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'کاهش وزن')
        self.assertEqual(response.context['selected_category_id'], self.category.id)

    def test_goal_filter(self):
        response = self.client.get(reverse('core:home'), {'goal': self.goal.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ورزش صبح')
        self.assertEqual(response.context['selected_goal_id'], self.goal.id)
    
    def test_pagination(self):
        for i in range(5):
            Goal.objects.create(
                user=self.user,
                title=f'هدف {i}',
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=30)
            )
        response = self.client.get(reverse('core:home'), {'goals_page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('goals' in response.context)
        self.assertLessEqual(len(response.context['goals']), 3)
    
    def test_goal_create(self):
        data = {
            'title': 'یادگیری پایتون',
            'description': 'یادگیری Django',
            'start_date': '2025-05-14',
            'end_date': '2025-06-14',
            'categories': [self.category.id],
            'progress': '0',
        }
        response = self.client.post(reverse('core:goal_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Goal.objects.filter(title='یادگیری پایتون').exists())
    
    def test_habit_create(self):
        data = {
            'title': 'ورزش روزانه',
            'frequency': 'daily'
        }
        response = self.client.post(reverse('core:habit_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Habit.objects.filter(title='ورزش روزانه').exists())

    def test_task_create(self):
        data = {
            'title': 'تمرین کدنویسی',
            'priority': 'medium',
            'status': 'pending',
            'due_date': '2025-05-15',
            'goal': self.goal.id
        }
        response = self.client.post(reverse('core:task_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='تمرین کدنویسی').exists())
    
    def test_category_create(self):
        data = {'name': 'کار'}
        response = self.client.post(reverse('core:category_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='کار').exists())

    def test_history_view(self):
        response = self.client.get(reverse('core:history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/history.html')
        self.assertTrue('habit_statuses' in response.context)
        self.assertTrue('task_statuses' in response.context)

    def test_calendar_events(self):
        response = self.client.get(reverse('core:calendar_events'))
        self.assertEqual(response.status_code, 200)
        events = json.loads(response.content)
        self.assertTrue(any(event['title'] == 'ورزش صبح' for event in events))
        self.assertTrue(any(event['title'] == 'مطالعه روزانه' for event in events))
    
    def test_habit_viewset_list(self):
        response = self.api_client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]['title'], 'مطالعه روزانه')
    
    def test_habit_viewset_toggle(self):
        today = timezone.now().date().strftime('%Y-%m-%d')
        response = self.api_client.post(f'/api/habits/{self.habit.id}/toggle/')
        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertIn(today, self.habit.done_dates)

