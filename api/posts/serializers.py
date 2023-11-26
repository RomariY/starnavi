from rest_framework import serializers

from api.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer
    """

    def create(self, validated_data):
        """
        Set owner to authenticated user
        """
        validated_data["owner"] = self.context.get("request").user.userprofile
        return super().create(validated_data)

    class Meta:
        model = Post
        fields = (
            "id",
            "photo",
            "title",
            "caption",
            "location",
            "likes_count",
            "owner",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )
