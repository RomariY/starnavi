from django.db import models
from django.contrib.auth.models import User

from api.utils.models import UUIDModel, TimeStamp


class UserProfile(UUIDModel, TimeStamp):
    """
    Represents a user profile model

    user (User): user instance which is related to this profile and contains basic user information
                 like email, first_name, last_name
    bio (str): user bio information
    phone (str): user phone number
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def email(self):
        return self.user.email

    @property
    def last_login(self):
        return self.user.last_login

    def __str__(self):
        return self.email
