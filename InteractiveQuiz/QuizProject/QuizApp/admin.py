from django.contrib import admin
from .models import Quiz, Category, Question, Choice, Answer, Result

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category',)  # Display these fields in the admin panel


# Register the remaining models
admin.site.register(Quiz)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Result)


