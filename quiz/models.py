from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    total_timer = models.IntegerField(default=60, help_text="Загальний таймер для всіх питань (в секундах)")
    total_time = models.IntegerField(default=60)
    question_count = models.IntegerField(default=0, help_text="Кількість питань")
    logo = models.ImageField(upload_to='quiz/logos/', blank=True, null=True)  # мультимедіа для вікторини
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    time_limit = models.IntegerField(default=30, help_text="Таймер для питання (в секундах)")
    order = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='questions/photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='answers/photos/', blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(default=timezone.now)
