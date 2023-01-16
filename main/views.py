from rest_framework.viewsets import ModelViewSet

from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response

from .serializers import RestaurantSerializer, PostSerializer
from .models import Restaurant, Post
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from rest_framework import filters

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset() # Product.objects.all()
        if q:
            queryset = queryset.filter(Q(title__icontains=q))

        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


