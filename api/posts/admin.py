from django.contrib import admin

from api.posts.models import Post, Like
from api.users.models import UserProfile


class LikesInline(admin.TabularInline):
    model = Like
    verbose_name = "Like"
    verbose_name_plural = "Likes"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "caption",
        "hidden",
        "owner",
    )
    inlines = [
        LikesInline,
    ]
    exclude = ["likes"]
    list_filter = ("created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "owner")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user.userprofile
        return super().save_model(request, obj, form, change)
