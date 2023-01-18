from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostCommentsViewSet, RestourantCommentsViewSet, CreateRatingAPIView, favorites_list


router = DefaultRouter()

router.register('post-comments', PostCommentsViewSet)
router.register('rest-comments', RestourantCommentsViewSet)
# router.register('favorites', favorites_list)

urlpatterns = [
    path('', include(router.urls)),
    path('rating/', CreateRatingAPIView.as_view()),
    path('favorites/', favorites_list),
]