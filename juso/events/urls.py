from django.urls import path

from juso.events import views
from juso.webpush import views as webpush

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event-list"),
    path("subscribe/", webpush.subscribe_to_webpush, name="webpush-subscribe"),
    path("unsubscribe/", webpush.unsubscribe_from_webpush, name="webpush-unsubscribe"),
    path("is-subscribed/", webpush.is_subscribed, name="webpush-is-subscribed"),
    path("section/<int:pk>/", views.event_list_for_section, name="section-event-list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.event_detail,
        name="event-detail",
    ),
    path("ical/", views.event_list_ical, name="event-list-ical",),
    path("location/<slug:slug>/", views.location_detail, name="location-detail"),
]
