from django.urls import path

from juso.events import views

app_name = "events"

urlpatterns = [
    path('', views.event_list, name="event-list"),
    path('section/<int:pk>/',
         views.event_list_for_section,
         name="section-event-list"),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.event_detail, name="event-detail"
    ),
    path('location/<slug:slug>/',
         views.location_detail,
         name="location-detail")
]
