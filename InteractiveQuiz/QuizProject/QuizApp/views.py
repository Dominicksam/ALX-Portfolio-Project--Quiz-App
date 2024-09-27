from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import RegisterForm, QuizForm, QuestionForm
from .models import Question, Category, Result, Quiz, UserAnswer

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
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    quizzes = Quiz.objects.all()

    if category_id:
        quizzes = quizzes.filter(category_id=category_id)

    return render(request, 'accounts/home.html', {
        'categories': categories,
        'quizzes': quizzes
    })

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

# Protected Page
class ProtectedView(TemplateView):
    template_name = 'accounts/protected.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Main Quiz View
@login_required
def quiz_view(request, quiz_id):
    # Get the quiz object
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Get the list of questions associated with the quiz
    questions = quiz.get_questions()  # Returns a queryset

    if request.method == 'POST':
        user_answers = {}  # This will store user's answers as {question.id: selected_option}

        # Loop through each question to get the user's selected option
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option:
                user_answers[question.id] = int(selected_option)  # Ensure this is stored as an integer

                # Save the user's answer to the database
                UserAnswer.objects.create(
                    user=request.user,  # This should be the logged-in user
                    question=question,
                    selected_option=selected_option,
                    quiz=quiz
                )

        # Calculate the score by comparing correct answers with user's answers
        score = calculate_score(questions, user_answers)
        
        # Save the result to the database
        Result.objects.create(user=request.user, quiz=quiz, score=score)

        # Render the result page, passing the quiz, score, questions, user answers, and correct answers
        return render(request, 'quiz/result.html', {
            'quiz': quiz,
            'score': score,
            'questions': questions,
            'user_answers': user_answers,
            'correct_answers': {question.id: question.correct_option for question in questions},  # Include correct answers
        })

    # If it's a GET request, show the quiz form
    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions,
    })
    
def calculate_score(questions, user_answers):
    correct_answers = 0

    for question in questions:
        correct_option = question.correct_option  # The correct answer stored in the DB
        user_option = user_answers.get(question.id)  # The user's selected answer

        # Check if the user answer is correct
        if user_option is not None and user_option == correct_option:
            correct_answers += 1

    return correct_answers

# Quiz List View
@login_required
def quiz_list_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

# User Quiz History
@login_required
def user_quiz_history(request):
    # Get the logged-in user's previous quiz results
    previous_results = Result.objects.filter(user=request.user).order_by('-date_taken')
    
    # Create a list to hold the result data with user answers
    history_with_answers = []

    for result in previous_results:
        user_answers = UserAnswer.objects.filter(user=result.user, quiz=result.quiz)
        history_with_answers.append({
            'result': result,
            'user_answers': user_answers
        })

    return render(request, 'quiz/quiz_history.html', {'history': history_with_answers})

