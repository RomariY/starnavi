import uuid
from django.db import models


class UUIDModel(models.Model):
    """
    Base abstract model that provides 'uuid' primary key field to replace the default PK
        and created_at field to have objects creation dates
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"


class CreateTimeModel(models.Model):
    """
    Represents a basic model which store information about creation time
    """

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True, editable=False, null=True)

    class Meta:
        abstract = True


class TimeStamp(models.Model):
    """
    Represents a basic model which store information about time
    """

    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True, editable=False, null=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True, editable=False, null=True)

    class Meta:
        abstract = True
