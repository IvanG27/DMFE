from django.urls import path
from DMFEApp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "DMFEApp"

urlpatterns = [
    path('home.html', views.home, name="Home"),
    path('instructions.html', views.instructions, name="Instructions"),
    path('eda.html', views.eda, name="EDA"),
    path('pca.html', views.pca, name="PCA"),
    path("", views.uploadFile, name = "uploadFile"),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )

