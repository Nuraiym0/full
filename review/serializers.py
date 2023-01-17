from rest_framework.serializers import ModelSerializer

from .models import PostComments, RestourantComments, RatingRestourant, RestourantFavorites


class RestourantCommentSerializer(ModelSerializer):
    class Meta:
        model = RestourantComments
        fields = ('__all__')


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs


class PostCommentsSerializer(ModelSerializer):
    class Meta:
        model = PostComments
        fields = ('__all__')


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()

        return rep


class RatingRestourantSerializer(ModelSerializer):
    class Meta:
        model = RatingRestourant
        fields = ('__all__')


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['author'] = request.user

        return attrs


class RestourantFavoritesSerializer(ModelSerializer):
    class Meta:
        model = RestourantFavorites
        fields = ('restourant',)
