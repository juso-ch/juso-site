from django.urls import path

from juso.events import views

app_name = "events"

urlpatterns = [
    path('', views.event_list, name="event-list"),
    path('<slug:slug>/', views.event_detail, name="event-detail"),
    path('location/<slug:slug>/',
         views.location_detail,
         name="location-detail")
]
