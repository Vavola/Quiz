from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    time_limit = models.IntegerField(default=30)
    question_type = models.CharField(max_length=50, choices=(('text', 'Text'), ('image', 'Image'), ('video', 'Video')))
    image = models.ImageField(upload_to='questions/images/', blank=True, null=True)
    video = models.FileField(upload_to='questions/videos/', blank=True, null=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(default=now)