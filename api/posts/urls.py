from api.posts.views import PostsViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=True)
router.register(r"post", PostsViewSet, basename="post")
urlpatterns = router.urls
