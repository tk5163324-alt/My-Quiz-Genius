from django.contrib import admin
from .models import Profile, Question, QuizAttempt

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(QuizAttempt)