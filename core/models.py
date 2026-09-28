from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    answer = models.CharField(max_length=255)

    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.question


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)

    total_questions = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"



class AttemptedQuestion(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )

    attempted_at = models.DateTimeField(
        auto_now_add=True
    )