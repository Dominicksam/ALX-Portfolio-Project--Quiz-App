from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # User authentication routes
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/protected/', views.ProtectedView.as_view(), name='protected'),  # Example of protected view

    # Quiz-related routes
    path('quizzes/', views.quiz_list_view, name='quiz_list'),  # List all quizzes
    path('quizzes/<int:quiz_id>/', views.quiz_view, name='quiz_view'),  # Take a specific quiz
    path('quizzes/add/', views.add_quiz_view, name='add_quiz'),  # Add a new quiz
    path('quizzes/<int:quiz_id>/add-question/', views.add_question_view, name='add_question'),  # Add question to a quiz
    path('quizzes/<int:quiz_id>/detail/', views.quiz_detail_view, name='quiz_detail'),  # Quiz details

    # User scores route
    path('user/scores/', views.user_scores_view, name='user_scores'),  # View user's quiz scores
]
