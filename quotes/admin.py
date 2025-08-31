from django.contrib import admin
from .models import Quote, PageView, Comment, Rating

# Регаем модели в админке
admin.site.register(Quote)
admin.site.register(PageView)
admin.site.register(Comment)
admin.site.register(Rating)
