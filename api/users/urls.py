from api.users.views import UserProfileViewSet, SignUpViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=True)
router.register(r"profile", UserProfileViewSet, basename="profile")
router.register(r"sign-up", SignUpViewSet, basename="sign-up")
urlpatterns = router.urls
