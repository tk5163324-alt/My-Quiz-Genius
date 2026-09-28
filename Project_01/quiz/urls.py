from django.urls import path
from . import views


urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path("quiz/", views.start_quiz, name="start_quiz"),
   
    path("leaderboard/", views.leaderboard, name="leaderboard"),

    path("profile/", views.profile, name="profile"),

    path("login/", views.user_login, name="login"),

]