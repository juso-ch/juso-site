from django.urls import path

from juso.blog import views
from juso.webpush import views as webpush

app_name = "blog"

urlpatterns = [
    path("", views.article_list, name="article-list"),
    path("subscribe/", webpush.subscribe_to_webpush, name="webpush-subscribe"),
    path("unsubscribe/",
         webpush.unsubscribe_from_webpush,
         name="webpush-unsubscribe"),
    path("is-subscribed/", webpush.is_subscribed,
         name="webpush-is-subscribed"),
    path("rss/", views.ArticleFeed(), name="rss-feed"),
    path("<slug:slug>/", views.article_detail, name="article-detail"),
]
