from rest_framework import serializers

from .models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'created_at', 'user_id', 'username']
        read_only_fields = ['id', 'created_at', 'user_id', 'username']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionDetailSerializer(QuestionSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ['answers']

