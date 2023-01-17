from django_filters.rest_framework import FilterSet
import django_filters

from .models import Restaurant, Post


class RestourantFilter(FilterSet):
    cuisine = django_filters.CharFilter(field_name='cuisine')
    rating = django_filters.DateFilter(field_name='rating')


    class Meta:
        model = Restaurant
        fields = ['cuisine', 'rating']


class PostFilter(FilterSet):
    price = django_filters.DateFilter(field_name='price')
    cuisine = django_filters.CharFilter(field_name='cuisine')


    class Meta:
        model = Post
        fields = ['price', 'cuisine']
