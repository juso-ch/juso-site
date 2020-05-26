from django.urls import path

from juso.blog import views

app_name = "blog"

urlpatterns = [
    path('', views.article_list, name="article-list"),
    path('rss/', views.ArticleFeed(), name="rss-feed"),
    path('<slug:slug>/', views.article_detail, name="article-detail"),
]
