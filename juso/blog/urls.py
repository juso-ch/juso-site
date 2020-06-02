from django.urls import path

from juso.blog import views

app_name = "blog"

urlpatterns = [
    path('', views.article_list, name="article-list"),
    path('subscribe/', views.subscribe_to_webpush, name="webpush-subscribe"),
    path('unsubscribe/', views.unsubscribe_from_webpush,
         name="webpush-unsubscribe"),
    path('is-subscribed/', views.is_subscribed,
         name="webpush-is-subscribed"),
    path('rss/', views.ArticleFeed(), name="rss-feed"),
    path('<slug:slug>/', views.article_detail, name="article-detail"),
]
