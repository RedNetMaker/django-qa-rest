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


class AnswerAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='responder', password='password123')
        self.other_user = User.objects.create_user(username='other', password='password123')
        self.question = Question.objects.create(text='What is Django REST Framework?')

    def test_authenticated_user_can_create_answer(self):
        url = reverse('question-answer-create', args=[self.question.id])
        payload = {'text': 'It is a toolkit for building Web APIs.'}

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, payload, format='json')
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.get()
        self.assertEqual(answer.text, payload['text'])
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['question_id'], self.question.id)

    def test_create_answer_requires_authentication(self):
        url = reverse('question-answer-create', args=[self.question.id])
        payload = {'text': 'Anonymous answers are not allowed.'}

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Answer.objects.count(), 0)

    def test_get_answer_detail_returns_answer_data(self):
        answer = Answer.objects.create(question=self.question, user=self.user, text='Example answer')

        url = reverse('answer-detail', args=[answer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], answer.id)
        self.assertEqual(response.data['text'], answer.text)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['question_id'], self.question.id)

    def test_owner_can_delete_answer(self):
        answer = Answer.objects.create(question=self.question, user=self.user, text='Delete me')

        url = reverse('answer-detail', args=[answer.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Answer.objects.filter(id=answer.id).exists())

    def test_non_owner_cannot_delete_answer(self):
        answer = Answer.objects.create(question=self.question, user=self.user, text='Protected answer')

        url = reverse('answer-detail', args=[answer.id])
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(url)
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Answer.objects.filter(id=answer.id).exists())