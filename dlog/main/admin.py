from django.contrib import admin
from .models import User, Article, Comment

# Регистрация моделей в админке
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Comment)
#admin.site.register(Category)
