from django.urls import path

from juso.people import views

app_name = 'people'

urlpatterns = [
    path('person/<int:pk>/', views.person_detail, name="person-detail"),
    path('team/<int:pk>/', views.team_detail, name="team-detail"),
    path('', views.teams_for_section, name="section-team-list"),
]
