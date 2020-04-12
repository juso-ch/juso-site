from django.urls import path

from juso.forms import views

app_name = "forms"

urlpatterns = [
    path('<pk:pk>/', views.form_detail, name="form-detail"),
]
