from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow

MIN_TEXT_LENGTH = 5
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')

class FollowSerializer(serializers.ModelSerializer):
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