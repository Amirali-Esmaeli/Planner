# Generated by Django 5.2 on 2025-05-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='done',
        ),
        migrations.AddField(
            model_name='habit',
            name='done_dates',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
