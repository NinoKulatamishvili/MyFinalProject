from django.contrib import admin
from .models import Products, Categories, User, Gender, Comment
# Register your models here.
admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(User)
admin.site.register(Gender)
admin.site.register(Comment)