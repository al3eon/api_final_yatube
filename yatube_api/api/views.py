from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .permissions import IsAuthorOrReadOnly
# А импорты из другого приложения нужно отделять?
# И с вопросами как удобнее, в личку или так?
from posts.models import Comment, Follow, Group, Post
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class AuthorPermissionViewSet(viewsets.ModelViewSet):
    """Базовый ViewSet для моделей с автором."""
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(AuthorPermissionViewSet):
    """ViewSet для работы с постами.

    Разрешает редактирование и удаление только автору поста"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination


class CommentViewSet(AuthorPermissionViewSet):
    """ViewSet для работы с комментариями к постам.

    Разрешает редактирование и удаление только автору комментария."""

    # Я так понял, из-за переопределения метода get_queryset
    # его можно тут не указывать. Можно ли его отсюда убрать?
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_post(self):
        """Возвращает пост."""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает queryset комментариев для текущего поста."""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """Создаёт комментарий с привязкой к текущему пользователю и посту."""
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet для управления подписками пользователя."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает только подписки текущего пользователя."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создаёт подписку с привязкой к текущему пользователю."""
        serializer.save(user=self.request.user)
