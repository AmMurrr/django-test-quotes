from django.db import models
from django.db.models import F
from django.db.models.functions import Lower

# модель для цитат
class Quote(models.Model):
    text = models.TextField()  
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def update_likes(self, change=1):
        Quote.objects.filter(id=self.id).update(likes=F('likes') + change)
        self.refresh_from_db()
    
    def update_dislikes(self, change=1):
        Quote.objects.filter(id=self.id).update(dislikes=F('dislikes') + change)
        self.refresh_from_db()

    def __str__(self):
        return f'"{self.text}" - {self.source}'


# для счётчика просмотров страниц
class PageView(models.Model):
    name = models.CharField(max_length=100, unique=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.views}'


    def increment(name="quotes"):
        obj, _ = PageView.objects.get_or_create(name=name)
        obj.views = F('views') + 1
        obj.save()
        obj.refresh_from_db()
        return obj.views
    
    def get_views(name="quotes"):
        obj, _ = PageView.objects.get_or_create(name=name)
        return obj.views

# модель для комментариев к цитатам
class Comment(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.CharField(max_length=100)                              
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on "{self.quote.text}" at {self.created_at}'

# модель для оценок сайта 
class Rating(models.Model):
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.score}'