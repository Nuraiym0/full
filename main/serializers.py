from rest_framework.serializers import ModelSerializer

# from rest_framework import serializers

from .models import Restaurant, Post, Category, Orders, OrderUpdate#, Subscription


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
        rep['restourant'] = CategorySerializers(instance.restourant_name).data
        rep['cuisine'] = CategorySerializers(instance.cuisine).data
        rep['restourant'] = RestaurantSerializer(instance.cuisine).data

        return rep


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['post'] = PostSerializer(instance.post).data
        
        return rep


class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


    def to_representation(self, instance):
        return super().to_representation(instance)
        

class OrderUpdateSerializer(ModelSerializer):
    class Meta:
        model = OrderUpdate
        fields = '__all__'


    def to_representation(self, instance):
        return super().to_representation(instance)


# class SubscriptionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Subscription
#         fields = '__all__'
    

#     def validate(self, attrs):
#         restourant = attrs.get('restourant')
#         subs = attrs.get('subscribe')

#         if Subscription.objects.filter(restourant=restourant, subscribe=subs).exists():
#             Subscription.objects.filter(restourant=restourant, subscribe=subs).delete()
#         else:
#             Subscription.objects.create(restourant=restourant, subscribe=subs)
        
#         return attrs


# class SubscribeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Subscription
#         fields = ('restourant',)


# class SubscriberSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Subscription
#         fields = ('restourant',)


