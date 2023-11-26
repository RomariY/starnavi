from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.users.models import UserProfile
from api.utils.validators import PasswordValidatorMixin, PhoneValidatorMixin


class BaseUserSerializer(PhoneValidatorMixin, serializers.Serializer):
    """
    Represents a base validation for User model
    """
    email = serializers.EmailField(source='user.email', required=True)
    first_name = serializers.CharField(source='user.first_name', required=True, max_length=150)
    last_name = serializers.CharField(source='user.last_name', required=True, max_length=150)

    def validate_email(self, value):
        user = self.context.get("request").user

        if user.is_authenticated and user.email == value:
            raise ValidationError("Provide the email that not equals to yours.")
        if User.objects.filter(username=value).exists():
            raise ValidationError('User with this email already exists.')
        return value


class SignUpSerializer(PasswordValidatorMixin, BaseUserSerializer, serializers.ModelSerializer):
    """
    Represents a validation for UserProfile model once it's creating
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def create(self, validated_data):
        user_data = validated_data.pop("user", {})
        user_data.update(dict(username=user_data.get('email')))

        user = User(**user_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        validated_data.update(user=user)
        obj = super().create(validated_data)
        return obj

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "bio",
            "phone",
        )
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(BaseUserSerializer, serializers.ModelSerializer):
    """
    Represents a validation for UserProfile model once it's updating
    """

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        email = user_data.get('email')
        if email:
            user_data.update(dict(username=email))

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        obj = super().update(instance, validated_data)
        return obj

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "bio",
            "phone",
        )
