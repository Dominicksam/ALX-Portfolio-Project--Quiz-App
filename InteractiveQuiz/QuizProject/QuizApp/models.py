from django.db import models
from django.contrib.auth.models import User

DIFF_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'), 
)

class Category(models.Model):
    """Represents a quiz category"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    """Represents a quiz under a category"""
    name = models.CharField(max_length=200, default='New Quiz') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, default='General')
    number_of_questions = models.IntegerField(default=10)
    time = models.IntegerField(help_text="Duration of the quiz in minutes", default=30)
    required_score_to_pass = models.IntegerField(help_text="Required score in percentage", default=50)
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES, default='easy')
    

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    def get_questions(self):
        """Get all questions related to the quiz"""
        return self.questions.all()

"""
class Question(models.Model):
    #Represents a quiz question#
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default='Question Text')
"""

class Question(models.Model):
    """Represents a single question in a quiz."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255, default='Option 1')
    option2 = models.CharField(max_length=255, default='Option 2')
    option3 = models.CharField(max_length=255, default='Option 3')
    option4 = models.CharField(max_length=255, default='Option 4')
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], default=1)

    def __str__(self):
        return self.text

    def get_options(self):
        """Returns a list of all options."""
        return [self.option1, self.option2, self.option3, self.option4]

class UserAnswer(models.Model):
    """Represents a user's answer to a specific question."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.question.text} - Option {self.selected_option}'


class Result(models.Model):
    """Represents a user's quiz result"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.name} - {self.score}'

    def passed(self):
        """Check if the user passed the quiz based on the required score"""
        return self.score >= self.quiz.required_score_to_pass