from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view, 
    )  

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('<int:pk>/', quiz_view, name='quiz-view'),
    path('<int:pk>/data/', quiz_data_view, name='quiz-data-view'),
]



#from django.urls import path
#from . import views

#urlpatterns = [
#    path('', views.main_view, name='main-view'),  # Your main view
#    path('<int:pk>/', views.quiz_view, name='quiz-view'),  # View for a quiz with an integer primary key
#]
