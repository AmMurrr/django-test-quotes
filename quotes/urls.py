from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.random_quote_view, name='random_quote'),
    path('add/', views.add_quote_view, name='add_quote'),
    path('top/', views.top_quotes_view, name='top_quotes'),
    path('top-sources/', views.top_sources_view, name='top_sources'),
    path('like/<int:quote_id>/', views.like_quote, name='like_quote'),
    path('dislike/<int:quote_id>/', views.dislike_quote, name='dislike_quote'),
    path('comment/add/<int:quote_id>/', views.add_comment, name='add_comment'),
    path('rate/', views.submit_rating, name='submit_rating'),
]