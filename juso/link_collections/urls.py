from django.urls import path

from juso.link_collections import views

app_name = "collection"

urlpatterns = [
    path("", views.collection_view, name="collection-detail"),
]
