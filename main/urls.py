from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RestaurantViewSet, PostViewSet
from . import views

router = DefaultRouter()

router.register('restaurant', RestaurantViewSet)
router.register('post', PostViewSet)

urlpatterns =[
    path('', include(router.urls)),
    # path('', views.index, name='index.html'),
]
