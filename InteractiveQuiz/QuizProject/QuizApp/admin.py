from django.contrib import admin
from .models import Quiz, Category, Question, UserAnswer, Result

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Register Quiz model
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'required_score_to_pass')
    list_filter = ('category',)
    search_fields = ('name',)


# Register Question model
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'category', 'correct_option')
    list_filter = ('quiz', 'category')
    search_fields = ('text',)

    # Custom admin action to view the options directly in the question list
    def display_options(self, obj):
        return f"{obj.option1}, {obj.option2}, {obj.option3}, {obj.option4}"

    display_options.short_description = 'Options'


# Register UserAnswer model
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_option')
    list_filter = ('question', 'user')
    search_fields = ('user__username', 'question__text')


# Register Result model
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'date_taken')
    list_filter = ('quiz', 'user')
    search_fields = ('user__username', 'quiz__name')
