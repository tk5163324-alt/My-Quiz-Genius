from django.urls import path
from core import views


urlpatterns = [

    # Home
    path(
        '',
        views.base,
        name='base'
    ),

    # Quiz generation
    path(
        'generate/',
        views.generate,
        name='generate'
    ),

    # Quiz
    path(
        'quiz/',
        views.quiz,
        name='quiz'
    ),

    # Submit answer
    path(
        'submit-answer/',
        views.submit_answer,
        name='submit_answer'
    ),

    # Leaderboard
    path(
        'leaderboard/',
        views.leaderboard,
        name='leaderboard'
    ),

    # Profile
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # Authentication
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
]