from django.urls import path
from . import views

urlpatterns = [
    # Home and Information Pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('medal/', views.medalWinners, name='medal'),
    path('countriesWinners/', views.winnersCountries, name='countriesWinners'),
    path('games/', views.games, name='games'),
    path('players/', views.players, name='players'),
    path('highlights/', views.highlights, name='highlights'),
    path('opening/', views.opening, name='opening'),
    path('closing/', views.closing, name='closing'),
    path('torch/', views.torch, name='torch'),
    path('gamesD/', views.gamesD, name='gamesD'),

    # Custom Authentication URLs
    path('login/', views.login_view, name='login'),  # Custom login view
    path('signup/', views.signup_view, name='signup'),  # Custom signup view
    path('logout/', views.user_logout, name='logout'),  # Custom logout view

    # Quiz-related URLs
    path('take_quiz/', views.take_quiz_view, name='take_quiz'),
    path('quiz_results/<int:quiz_attempt_id>/', views.quiz_results_view, name='quiz_results'),
    path('view_past_quizzes/', views.view_past_quizzes, name='view_past_quizzes'),
    path('dashboard/', views.dashboard_profile, name='dashboard'),

    # Game-related URLs
    path('game/', views.game_view, name='game'),
    path('save-score/', views.save_score, name='save_score'),
    path('clear_scores/', views.clear_scores, name='clear_scores'),
    path('delete_score/<int:score_id>/', views.delete_hurdle_score, name='delete_score')
]
