from django.urls import path

from .views import QuestionListCreateView, QuestionRetrieveDestroyView


urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionRetrieveDestroyView.as_view(), name='question-detail'),
]