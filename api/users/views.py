from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.users.models import UserProfile
from api.users.serializers import SignUpSerializer, UserProfileSerializer


class SignUpViewSet(CreateModelMixin, GenericViewSet):
    """
    Represents a view for signing up a new user
    """
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class UserProfileViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    """
    Represents a view for retrieving, updating and deleting a user profile
    """
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserProfile.objects.filter(user=user)
        return UserProfile.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
