from django.urls import path
from .views import quiz_view, result_view, quiz_list, quiz_detail  # Importing specific views directly or
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('', quiz_view, name='quiz'),
    path('result/', result_view, name='result'),
    path('quizzes/', quiz_list, name='quiz_list'),  # No need for 'views.' prefix since it's directly imported
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),  # Same here
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
