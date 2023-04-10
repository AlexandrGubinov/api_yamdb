from django.contrib import admin

from users.models import User
from reviews.models import Category, Genre, Review, Comment, Title 

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
