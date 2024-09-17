from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('', views.home_view, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/protected/', views.ProtectedView.as_view(), name='protected'),
    path('quizzes/', views.quiz_list_view, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),
    path('quiz/add/', views.add_quiz_view, name='add_quiz'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question_view, name='add_question'),
    path('quiz/<int:category_id>/', views.quiz_view, name='quiz'),
]




