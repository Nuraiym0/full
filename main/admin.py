from django.contrib import admin
from .models import *

class RestaurantLine(admin.TabularInline):
    model = Restaurant

class PostLine(admin.TabularInline):
    model = Post

admin.site.register(Restaurant)
admin.site.register(Post)

