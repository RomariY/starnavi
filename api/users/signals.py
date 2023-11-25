from django.db.models.signals import post_save
from django.dispatch import receiver

from api.users.models import UserProfile


@receiver(post_save, sender=UserProfile)
def update_last_activity_on_sign_up(sender, instance, created, **kwargs):
    """
    Update last activity when user sign up
    """
    if created:
        instance.last_activity = instance.created_at
        instance.save(update_fields=["last_activity"])
