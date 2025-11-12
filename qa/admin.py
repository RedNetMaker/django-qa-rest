# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text',)
    readonly_fields = ('created_at',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user', 'text', 'created_at')
    list_filter = ('created_at', 'question', 'user')
    search_fields = ('text', 'user__username', 'user__email', 'question__text')
    readonly_fields = ('created_at',)

