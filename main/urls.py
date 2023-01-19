from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RestaurantViewSet, PostViewSet, OrdersViewSet, OrderUpdateViewSet
from . import views

router = DefaultRouter()

router.register('restaurant', RestaurantViewSet)
router.register('post', PostViewSet)
router.register('orders', OrdersViewSet)
router.register('orderupdate', OrderUpdateViewSet)

urlpatterns =[
    path('', include(router.urls)),
    # path('', views.index, name='index.html'),
]
