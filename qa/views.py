from django.db.models import Prefetch
from rest_framework import generics

from .models import Answer, Question
from .serializers import QuestionDetailSerializer, QuestionSerializer


class QuestionListCreateView(generics.ListCreateAPIView):
    """
    GET: список всех вопросов
    POST: создать новый вопрос
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    GET: получить вопрос и все ответы на него
    DELETE: удалить вопрос (вместе с ответами)
    """

    queryset = Question.objects.prefetch_related(
        Prefetch('answers', queryset=Answer.objects.select_related('user'))
    )
    serializer_class = QuestionDetailSerializer

