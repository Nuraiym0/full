from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAdminUser

from .serializers import RestaurantSerializer, PostSerializer, CategorySerializers, OrdersSerializer, OrderUpdateSerializer
from .models import Restaurant, Post, Orders, OrderUpdate
from .filters import RestourantFilter, PostFilter

from review.models import RestourantFavorites, PostFavorites, PostLike

User=get_object_or_404


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_class = RestourantFilter

    def get_permissions(self):
        if self.action in ['retrive', 'list', 'search']:
            return []
        return [IsAdminUser()]
    

    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset() 
        if q:
            queryset = queryset.filter(Q(title__icontains=q))

        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


    @action(['POST'], detail=False)
    def favourite(request):
        user_id = request.data.get('user')
        rest_id =request.data.get('rest')
        user = get_object_or_404(User, id = user_id)
        rest = get_object_or_404(Post , id = rest_id)

        if RestourantFavorites.objects.filter(rest=rest, user=user).exists():
            RestourantFavorites.objects.filter(rest=rest,user=user).delete()
        else:
            RestourantFavorites.objects.create(rest=rest,user=user)
        return Response(status=201)

    
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def get_permissions(self):
        if self.action in ['retrive', 'list', 'search']:
            return []
        return [IsAdminUser()]
        


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


    @action(['POST'], detail=False)
    def favourite(request):
        user_id = request.data.get('user')
        post_id =request.data.get('post')
        user = get_object_or_404(User, id = user_id)
        post = get_object_or_404(Restaurant , id = post_id)

        if PostFavorites.objects.filter(post=post, user=user).exists():
            PostFavorites.objects.filter(post=post,user=user).delete()
        else:
            PostFavorites.objects.create(post=post,user=user)
        return Response(status=201)


    @action(['PUT'], detail=True)
    def like(self, request, pk=None):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, id=pk)

        if PostLike.objects.filter(post=post, user=user).exists():
            PostLike.objects.filter(post=post, user=user).delete()
        else:
            PostLike.objects.create(post=post, user=user)

        return Response(status=201)


    @action(['POST'], detail=True)
    def category(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
       
        if post.user != request.user:
            raise NotAcceptable('Недостаточно прав')

        request.data._mutable = True
        request.data.update({'post': pk})
        serializer = CategorySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)



class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    
class OrderUpdateViewSet(ModelViewSet):
    queryset = OrderUpdate.objects.all()
    serializer_class = OrderUpdateSerializer

