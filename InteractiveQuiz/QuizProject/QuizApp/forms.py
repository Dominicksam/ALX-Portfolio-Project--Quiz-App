from django import forms
from django.contrib.auth.models import User
from .models import Question, Quiz

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


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'category', 'topic', 'number_of_questions', 'time', 'required_score_to_pass', 'difficulty']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
