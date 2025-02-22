# Generated by Django 5.1.1 on 2025-02-14 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_question_order_quiz_game_pin_quiz_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='question',
            name='video',
        ),
        migrations.AddField(
            model_name='question',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='questions/photos/'),
        ),
    ]
