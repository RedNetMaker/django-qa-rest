from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Answer, Question


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='password123')

    def test_get_questions_list_returns_all_questions(self):
        Question.objects.create(text='First question')
        Question.objects.create(text='Second question')

        url = reverse('question-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'], 'Second question')
        self.assertEqual(response.data[1]['text'], 'First question')

    def test_post_create_question_success(self):
        url = reverse('question-list-create')
        payload = {'text': 'How to write tests?'}

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.get()
        self.assertEqual(question.text, payload['text'])

    def test_get_question_detail_includes_answers(self):
        question = Question.objects.create(text='Explain Django REST')
        Answer.objects.create(question=question, user=self.user, text='Use DRF for APIs.')
        Answer.objects.create(question=question, user=self.user, text='Read docs.')

        url = reverse('question-detail', args=[question.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], question.text)
        self.assertIn('answers', response.data)
        self.assertEqual(len(response.data['answers']), 2)
        self.assertEqual({answer['text'] for answer in response.data['answers']},
                         {'Use DRF for APIs.', 'Read docs.'})

    def test_delete_question_removes_question_and_answers(self):
        question = Question.objects.create(text='Delete me?')
        Answer.objects.create(question=question, user=self.user, text='Yes.')

        url = reverse('question-detail', args=[question.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=question.id).exists())
        self.assertFalse(Answer.objects.exists())