from django.contrib import admin

from api.users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "bio",
        "full_name",
        "created_at",
    )
    list_filter = ("created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "last_activity")

