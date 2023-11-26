from django.utils import timezone
from rest_framework.authtoken.admin import User
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import AccessToken

from api.users.models import UserProfile


class UpdateLastActivityLoginMiddleware:
    """
    Update last activity/login when user sending request or `login or refresh token
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            UserProfile.objects.filter(user=request.user).update(last_activity=timezone.now())
        response = self.get_response(request)

        # TODO remake this \|/
        try:
            access_token = response.data.get("access")
            if request.path in (reverse("login"), reverse("token_refresh")) and access_token:
                decoded_token = AccessToken(response.data.get("access"))
                User.objects.filter(id=decoded_token.get("user_id")).update(last_login=timezone.now())
        except:
            pass

        return response
