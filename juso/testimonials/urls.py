from django.urls import path

from .views import create, index

app_name = "testimonials"

urlpatterns = [
    path("", index, name="index"),
    path("create/", create, name="create")
]
