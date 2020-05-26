from django.urls import path

from juso.pages import views

app_name = "pages"

urlpatterns = (
    path('<path:path>/', views.page_detail, name="page"),
    path('sitemap.xml', views.sitemap_index, name="sitemap-index-root"),
    path('<path:path>/sitemap.xml', views.sitemap_index, name="sitemap-index"),
    path('', views.page_detail, name="root"),
)
