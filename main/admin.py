from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class RestaurantLine(admin.TabularInline):
    model = Restaurant

class PostLine(admin.TabularInline):
    model = Post

class RestourantAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_show','description', 'cuisine', 'work_time', 'rating' ]
    list_filter = ['cuisine', 'rating'  ]

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.__name__ = 'cover'

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_show','description', 'price', 'cuisine' ]
    list_filter = ['price', 'cuisine' ]

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.__name__ = 'cover'



admin.site.register(Restaurant, RestourantAdmin)
admin.site.register(Post, PostAdmin)


