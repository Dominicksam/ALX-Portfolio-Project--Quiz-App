from django.contrib import admin
from .models import Quiz, Category, Question, Choice, Result

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register Quiz model
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'number_of_questions', 'time', 'difficulty')
    list_filter = ('category', 'difficulty')
    search_fields = ('name',)

# Register Question model
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'category')  # Display these fields in the admin panel
    list_filter = ('quiz', 'category')
    search_fields = ('text',)

# Register Choice model
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('text',)

# Register Result model
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'date_taken')
    list_filter = ('quiz', 'user')
    search_fields = ('user__username', 'quiz__name')

