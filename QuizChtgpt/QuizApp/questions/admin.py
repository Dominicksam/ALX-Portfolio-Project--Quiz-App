from django.contrib import admin
from django import forms
from .models import Question, Answer, Category, Quiz

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Number of extra forms to display for adding answers

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['text', 'created_at']
    search_fields = ['text']
    list_filter = ['created_at']
    ordering = ['-created_at']

    class Media:
        css = {
            'all': ('questions/css/custom_admin.css',)
        }

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'text':
            formfield.widget.attrs['class'] = 'custom-question'
        return formfield

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'answers':
            formfield.widget.attrs['class'] = 'custom-answer'
        return formfield

# Registering models with the admin site
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)  # Registering Question with the customized admin class
admin.site.register(Answer)
