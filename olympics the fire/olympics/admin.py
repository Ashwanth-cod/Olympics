from django.contrib import admin
from .models import QuizAttempt, QuizDetail

class QuizDetailInline(admin.TabularInline):
    model = QuizDetail
    extra = 1

class QuizAttemptAdmin(admin.ModelAdmin):
    inlines = [QuizDetailInline]
    list_display = ('user', 'score', 'total_questions', 'date_attempted')
