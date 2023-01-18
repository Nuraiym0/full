from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable, NotAuthenticated
from drf_yasg.utils import swagger_auto_schema


from .serializers import PostCommentsSerializer, RestourantCommentSerializer, RatingRestourantSerializer, RestourantFavoritesSerializer
from .models import PostComments, RestourantComments, RatingRestourant, RestourantFavorites

from main.permissions import IsAuthorOrReadOnly


User = get_user_model()


class PostCommentsViewSet(ModelViewSet):
    queryset = PostComments.objects.all()
    serializer_class = PostCommentsSerializer
    permission_classes = [IsAuthorOrReadOnly]
    

class RestourantCommentsViewSet(ModelViewSet):
    queryset = RestourantComments.objects.all()
    serializer_class = RestourantCommentSerializer
    permission_classes = [IsAuthorOrReadOnly]


class CreateRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RatingRestourantSerializer())
    def post(self, request):
        user = request.user
        ser = RatingRestourantSerializer(data=request.data, context={"request":request})
        ser.is_valid(raise_exception=True)
        lesson_id = request.data.get("lesson")
        if RatingRestourant.objects.filter(author=user, lesson__id=lesson_id).exists():
            raiting = RatingRestourant.objects.get(author=user, lesson__id=lesson_id)
            raiting.value = request.data.get("value")
            raiting.save()
        else:
            ser.save()
        return Response(status=201)


@api_view(['GET'])
def favorites_list(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated(detail='Authentication required')

    queryset = RestourantFavorites.objects.filter(user=request.user)
    serializer = RestourantFavoritesSerializer(queryset, many=True)

    return Response(serializer.data, status=200)
