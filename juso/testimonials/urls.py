from django.urls import path
from .views import index, create

app_name = "testimonials"

urlpatterns = [path("", index, name="index"), path("create/", create, name="create")]
