from rest_framework import serializers
from .models import Habit, Task
from django.utils import timezone

class HabitSerializer(serializers.ModelSerializer):
    is_done_today = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'title', 'frequency', 'created_at', 'is_done_today']
        read_only_fields = ['id', 'created_at', 'is_done_today']

    def get_is_done_today(self, obj):
        today = timezone.now().date().strftime('%Y-%m-%d')
        return today in obj.done_dates
    
    def validate_frequency(self, value):
        valid_choices = dict(Habit._meta.get_field('frequency').choices)
        if value not in valid_choices.keys():
            raise serializers.ValidationError("تکرار نامعتبر است")
        return value
       