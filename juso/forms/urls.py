from django.urls import path

from juso.forms import views

app_name = "forms"

urlpatterns = [
    path('<int:pk>/', views.form_view, name="form-detail"),
]
