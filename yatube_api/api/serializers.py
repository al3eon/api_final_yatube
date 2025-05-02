from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

MIN_TEXT_LENGTH = 5
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post"""

    author = SlugRelatedField(slug_field='username', read_only=True)
    text = serializers.CharField(
        min_length=MIN_TEXT_LENGTH,
        error_messages={
            'min_length': ('Текст поста должен содержать минимум '
                           f'{MIN_TEXT_LENGTH} символов!')
        }
    )

    class Meta:
        fields = ('id', 'pub_date', 'image', 'group', 'author', 'text')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    text = serializers.CharField(
        min_length=MIN_TEXT_LENGTH,
        error_messages={
            'min_length': ('Текст поста должен содержать минимум '
                           f'{MIN_TEXT_LENGTH} символов!')
        }
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ('post', )


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group"""
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow"""
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        user = self.context['request'].user

        if user == data['following']:
            raise ValidationError('Вы не можете подписаться на самого себя!')

        if Follow.objects.filter(
                user=user,
                following=data['following']
        ).exists():
            raise ValidationError('Вы уже подписаны!')

        return data
