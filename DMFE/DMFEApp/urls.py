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
    path("", views.uploadFile, name = "UploadFile"),
    path("file.html", views.listarArchivos, name = "Files"),
    path("deleteFile.html/<int:id_file>", views.deleteFile, name ="DeleteFile"),
    path("mostrarDatos.html/<int:id_file>", views.mostrarDatos, name ="MostrarDatos"),
    path("obtenerResultadosPCA.html/<int:id_file>", views.obtenerResultadosPCA, name ="ObtenerResultadosPCA"),
    path("resultadosPCA.html", views.resultadosPCA, name ="ResultadosPCA"),
    
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )

