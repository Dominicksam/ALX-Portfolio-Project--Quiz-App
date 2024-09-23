from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import RegisterForm, QuizForm, QuestionForm
from .models import Question, Category, Result, Quiz

# User Registration
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# User Login
def login_view(request):
    error_message = None
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or reverse('home')
            return redirect(next_url)
        else:
            error_message = "Invalid credentials"

    return render(request, 'accounts/login.html', {'error': error_message})

# User Logout
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('home')

# Home View with Category Selection
@login_required 
def home_view(request):
    category_name = request.GET.get('category')
    categories = Category.objects.all()
    questions = []

    if category_name:
        category = get_object_or_404(Category, id=category_name)
        questions = Question.objects.filter(category=category)

    return render(request, 'accounts/home.html', {
        'categories': categories,
        'questions': questions
    })

# List available quizzes by category
@login_required
def quiz_list_view(request):
    category_name = request.GET.get('category')
    quizzes = Quiz.objects.filter(category__name=category_name) if category_name else Quiz.objects.all()
    categories = Category.objects.all()
    return render(request, 'quiz/quiz.html', {'quizzes': quizzes, 'categories': categories})

# Display a quiz and handle submission
@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('choices')
    
    if request.method == 'POST':
        score = 0
        user_answers = request.POST  # Capture all user answers from POST data

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            correct_choice = question.choices.filter(is_correct=True).first()

            if correct_choice:  # Check if there's a correct choice
                if selected_option == str(correct_choice.id):
                    score += 1

        # Save the result in the Result model
        Result.objects.create(user=request.user, quiz=quiz, score=score)

        # Pass the quiz, questions, score, and user answers to the result template
        return render(request, 'quiz/result.html', {
            'quiz': quiz,
            'questions': questions,
            'score': score,
            'user_answers': user_answers,
        })

    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'questions': questions})

# View Quiz Details (for adding questions, etc.)
@login_required
def quiz_detail_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

# Add a new quiz
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

# Add questions to a quiz
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

# View user's quiz scores
@login_required
def user_scores_view(request):
    scores = Result.objects.filter(user=request.user)
    return render(request, 'quiz/user_scores.html', {'scores': scores})

class ProtectedView(TemplateView):
    template_name = 'accounts/protected.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
