from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'
    
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})

"""
def quiz_data_view(request, pk):
    Quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in Quiz.get_question():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})  
    return JsonResponse({
        'data': questions,  
        'time': Quiz.time,
    })
"""
"""
def quiz_data_view(request, pk):
    data = {
        'question': 'question',
        'answer': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
        'time': Quiz.objects.get(pk=pk).time,
        'difficulty': Quiz.objects.get(pk=pk).difficulty,
        'required_score_to_pass': Quiz.objects.get(pk=pk).required_score_to_pass,
        
    }
    return JsonResponse(data)

def quiz_data_view(request, pk):
    try:
        quiz = Quiz.objects.select_related('question').get(pk=pk)  
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    data = {
        'question': quiz.question.text,  
        'answer': list(quiz.question.answers.values_list('text', flat=True)),  
        'time': quiz.time,
        'difficulty': quiz.difficulty,
        'required_score_to_pass': quiz.required_score_to_pass,
    }
    return JsonResponse(data)
"""

def quiz_data_view(request, pk):
    try:
        quiz = Quiz.objects.prefetch_related('questions__answers').get(pk=pk)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    questions = []
    for question in quiz.questions.all():  # Assuming 'questions' is a related name for the quiz's questions
        answers = [answer.text for answer in question.answers.all()]  # Assuming 'answers' is a related name for question's answers
        questions.append({
            'question': question.text,  # Assuming 'text' is the field for question text
            'answers': answers
        })

    return JsonResponse({
        'data': questions,
        'time': quiz.time,
        'difficulty': quiz.difficulty,
        'required_score_to_pass': quiz.required_score_to_pass,
    })
