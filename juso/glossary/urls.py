from django.urls import path

from juso.glossary import views

app_name = "glossary"

urlpatterns = [
    path('', views.glossary, name="glossary"),
]
