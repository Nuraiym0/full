from rest_framework.serializers import ModelSerializer

from .models import Restaurant, Post


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        rep['rating'] = instance.rating
        # rep['subscribers'] = SubscriberSerializer(instance.subscribers.all(), many=True).data
        # rep['subscriptions'] = SubscribeSerializer(instance.subscriptions.all(), many=True).data

        return rep


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()



