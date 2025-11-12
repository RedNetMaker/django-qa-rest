from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionDetailSerializer, QuestionSerializer


class IsAnswerOwnerOrReadOnly(permissions.BasePermission):
    """
    Ограничение на внесение изменений владельцами ответов.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


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


class QuestionAnswerCreateView(generics.CreateAPIView):
    """
    POST: добавить ответ к вопросу
    """

    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Handle schema generation by drf-yasg
        if getattr(self, 'swagger_fake_view', False):
            return Answer.objects.none()
        return Answer.objects.filter(question_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        serializer.save(question=question, user=self.request.user)


class AnswerRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    GET: получить конкретный ответ
    DELETE: удалить ответ
    """

    queryset = Answer.objects.select_related('user', 'question')
    serializer_class = AnswerSerializer
    permission_classes = [IsAnswerOwnerOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAnswerOwnerOrReadOnly()]
        return super().get_permissions()
