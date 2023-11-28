from django.db import models

from api.utils.models import UUIDModel, TimeStamp


class Post(UUIDModel, TimeStamp):
    """
    Represents a post model

    photo (ImageField): the photo of the specific post
    owner (User): user instance which provides the author of the post
    caption (str): caption to the specific post
    location (str): post location if available
    likes (M2M): The users who liked the specific post
    """
    photo = models.ImageField(upload_to="posts", blank=True, null=True)
    title = models.CharField(max_length=100)
    caption = models.TextField(blank=True, null=True)
    owner = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True)

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title} | {self.owner.full_name}"


class Like(UUIDModel, TimeStamp):
    """
    Represents a like model

    user (User): user instance which provides the author of the like
    post (Post): post instance which provides the liked post
    """
    userprofile = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        related_name="likes",
        related_query_name="like",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.userprofile.full_name} | {self.post.title} | {self.created_at}"
