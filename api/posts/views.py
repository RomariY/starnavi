from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters import rest_framework as filters

from api.posts.filters import PostFilter
from api.posts.models import Post, Like
from api.posts.serializers import PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing, editing and deleting posts.
    """

    serializer_class = PostSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # search_fields = ['owner__user__first_name', 'email', 'profile__profession']
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.objects.filter(hidden=False)

    @swagger_auto_schema(
        methods=['POST'],
        operation_id='like_post',
    )
    @action(methods=['POST'], detail=True, url_path='like_post')
    def like_post(self, *args, **kwargs):
        post_id = kwargs.get('pk')
        userprofile = self.request.user.userprofile
        try:
            like_obj, _ = Like.objects.get_or_create(post_id=post_id, userprofile=userprofile)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=['POST'],
        operation_id='dislike_post',
    )
    @action(methods=['POST'], detail=True, url_path='dislike_post')
    def dislike_post(self, *args, **kwargs):
        post_id = kwargs.get('pk')
        userprofile = self.request.user.userprofile
        try:
            Like.objects.get(post_id=post_id, userprofile=userprofile).delete()
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
