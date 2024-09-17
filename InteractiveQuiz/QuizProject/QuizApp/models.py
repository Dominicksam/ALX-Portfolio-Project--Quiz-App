from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', related_name='questions', on_delete=models.CASCADE, default='Quiz')
    text = models.CharField(max_length=255, default='Question')
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answers_set.all()

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default='Choice')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Quiz(models.Model):
    name = models.CharField(max_length=120, default='New Quiz')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, default='General')
    number_of_questions = models.IntegerField(default=10)
    time = models.IntegerField(help_text="Duration of the quiz in minutes", default=30)
    required_score_to_pass = models.IntegerField(help_text="Required score in %", default=50)
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES, default='easy')
    
    
    def __str__(self):
        return f"{self.name} - {self.category}"
    
    def get_questions(self):
        return self.questions.all()

class Answer(models.Model):
    text = models.CharField(max_length=255, default='Answer')
    correct = models.BooleanField(default=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Answer: {self.text}, Correct: {self.correct}"


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.name} - {self.score}'

