from django import forms
from django.contrib.auth.models import User
from .models import Question, Quiz, Choice

# Registration form for new users
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')

        return cleaned_data


# Form to create and update quizzes
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'name', 
            'category', 
            'topic', 
            'number_of_questions', 
            'time', 
            'required_score_to_pass', 
            'difficulty'
        ]


# Form to create and update questions
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'quiz', 'text']


# Form to add and update choices for a question
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
