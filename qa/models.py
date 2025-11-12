from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Question model - вопрос
    """
    text = models.TextField(verbose_name="текст вопроса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text


class Answer(models.Model):
    """
    Answer model - ответ на вопрос
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="вопрос"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name="пользователь"
    )
    text = models.TextField(verbose_name="текст ответа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"
        ordering = ['-created_at']

    # def __str__(self):
    #     question_text = self.question.text[:30] if len(self.question.text) > 30 else self.question.text
    #     return f"Ответ на: {question_text}..."

