from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:

        Profile.objects.create(
            user=instance
        )




class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    profile_pic = models.ImageField(
        upload_to="profile/",
        default="profile/default.png"
    )


    def __str__(self):

        return self.user.username





class Category(models.Model):

    name = models.CharField(
        max_length=100
    )


    def __str__(self):

        return self.name





class Question(models.Model):

    DIFFICULTY = (

        ("Easy","Easy"),

        ("Medium","Medium"),

        ("Hard","Hard"),

    )


    category = models.ForeignKey(

        Category,

        on_delete=models.CASCADE

    )


    difficulty = models.CharField(

        max_length=20,

        choices=DIFFICULTY,

        default="Easy"

    )


    question = models.TextField()


    option1 = models.CharField(max_length=255)

    option2 = models.CharField(max_length=255)

    option3 = models.CharField(max_length=255)

    option4 = models.CharField(max_length=255)


    correct_answer = models.CharField(max_length=255)


    explanation = models.TextField(

        blank=True,

        null=True

    )


    def __str__(self):

        return self.question




from django.contrib.auth.models import User


class Attempt(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    category = models.CharField(
        max_length=100
    )


    score = models.IntegerField()


    total_questions = models.IntegerField()


    percentage = models.FloatField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.user.username