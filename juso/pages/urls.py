from django.urls import path
from django.views.decorators.cache import cache_page
from juso.pages import views

app_name = "pages"

urlpatterns = (
    path('<path:path>/', views.page_detail, name="page"),
    path('sitemap.xml', cache_page(60*60)(views.sitemap_index),
         name="sitemap-index-root"),
    path('<path:path>/sitemap.xml', cache_page(60*60)(views.sitemap_index),
         name="sitemap-index"),
    path('', views.page_detail, name="root"),
)
urlpatterns = (
    path('<path:path>/', views.page_detail, name="page"),
    path('sitemap.xml', cache_page(60*60)(views.sitemap_index),
         name="sitemap-index-root"),
    path('<path:path>/sitemap.xml', cache_page(60*60)(views.sitemap_index),
         name="sitemap-index"),
    path('', views.page_detail, name="root"),
)
