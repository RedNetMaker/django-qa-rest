from django.urls import path

from .views import (
    AnswerRetrieveDestroyView,
    QuestionAnswerCreateView,
    QuestionListCreateView,
    QuestionRetrieveDestroyView,
)


urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionRetrieveDestroyView.as_view(), name='question-detail'),
    path('questions/<int:pk>/answers/', QuestionAnswerCreateView.as_view(), name='question-answer-create'),
    path('answers/<int:pk>/', AnswerRetrieveDestroyView.as_view(), name='answer-detail'),
]