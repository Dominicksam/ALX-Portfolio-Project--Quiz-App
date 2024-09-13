from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Result, Category, Quiz
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def quiz_view(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        try:
            score = sum(
                1 for question in questions
                if (selected_answer := request.POST.get(f'question_{question.id}'))
                and question.answers.get(id=selected_answer).is_correct
            )
            Result.objects.create(user=request.user, score=score)
        except Question.DoesNotExist:
            messages.error(request, 'One of the questions does not exist.')
            return redirect('quiz_list')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('quiz_list')

        return redirect('result')

    return render(request, 'questions/quiz.html', {'questions': questions})


def result_view(request):
    # sorcery skip: remove-unnecessary-else, use-named-expression
    result = Result.objects.filter(user=request.user).last()
    if result:
        return render(request, 'questions/result.html', {'result': result})
    else:
        messages.error(request, 'No result found.')
        return redirect('questions/quiz_list')

def quiz_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    quizzes = Quiz.objects.filter(category__name=selected_category) if selected_category else Quiz.objects.all()

    return render(request, 'questions/quiz_list.html', {'quizzes': quizzes, 'categories': categories})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'questions/quiz_detail.html', {'quiz': quiz})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('quiz_list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'questions/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('quiz_list')
        else:
            messages.error(request, 'Login failed. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')
