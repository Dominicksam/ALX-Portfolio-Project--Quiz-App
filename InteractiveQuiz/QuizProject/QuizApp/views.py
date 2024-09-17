from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Question, Category, Result, Quiz
from .forms import QuizForm, QuestionForm



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid credentials"
    return render(request, 'accounts/login.html', {'error': error_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')


@login_required
def home_view(request):
    category_name = request.GET.get('category')
    categories = Category.objects.all()

    questions = []

    if category_name:
        category = Category.objects.filter(name=category_name).first()
        if category:
            questions = Question.objects.filter(category=category)

    return render(request, 'accounts/home.html', {
        'categories': categories,
        'questions': questions
    })


class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'accounts/protected.html')


@login_required
def quiz_list_view(request):
    category = request.GET.get('category')
    if category:
        quizzes = Quiz.objects.filter(category__name=category)
    else:
        quizzes = Quiz.objects.all()
    categories = Category.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes, 'categories': categories})


@login_required
def quiz_view(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)
    score = 0
    total_questions = questions.count()

    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_option:
                score += 1

        # Save score in the Result model
        Result.objects.create(user=request.user, quiz=category, score=score)

        return redirect('quiz_result', category_id=category.id, score=score)

    return render(request, 'quiz/quiz.html', {'category': category, 'questions': questions})


@login_required
def quiz_detail_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})


@login_required
def add_quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm()
    return render(request, 'quiz/add_quiz.html', {'form': form})


@login_required
def add_question_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form, 'quiz': quiz})


@login_required
def quiz_result_view(request, category_id, score):
    category = Category.objects.get(id=category_id)
    return render(request, 'quiz/quiz_result.html', {'category': category, 'score': score})


@login_required
def user_scores_view(request):
    scores = Result.objects.filter(user=request.user)
    return render(request, 'quiz/user_scores.html', {'scores': scores})
