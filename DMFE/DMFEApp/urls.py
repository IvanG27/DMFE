from django.urls import path
from DMFEApp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "DMFEApp"

urlpatterns = [
    #plantilla de home
    path('home.html', views.home, name="Home"),
    #plantilla de instrucciones
    path('instructions.html', views.instructions, name="Instructions"),
    #plantillas para el algoritmo EDA
    path('eda.html', views.eda, name="EDA"),
    path("mostrarDatosEDA.html/<int:id_file>", views.mostrarDatosEDA, name ="MostrarDatosEDA"),
    path("resultadosEDA.html", views.resultadosEDA, name ="ResultadosEDA"),
    #plantillas para el algoritmo PCA
    path('pca.html', views.pca, name="PCA"),
    path("mostrarDatosPCA.html/<int:id_file>", views.mostrarDatosPCA, name ="MostrarDatosPCA"),
    path("resultadosPCA.html", views.resultadosPCA, name ="ResultadosPCA"),
    #plantillas para archivos
    path("uploadFile.html", views.uploadFile, name = "UploadFile"),
    path("file.html", views.listarArchivos, name = "Files"),
    path("deleteFile.html/<int:id_file>", views.deleteFile, name ="DeleteFile"),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )

