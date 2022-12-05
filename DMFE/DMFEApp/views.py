from django.shortcuts import render,HttpResponse
from django.conf import settings
from . import models
from django.core.files.storage import FileSystemStorage
import pandas as pd
import pandas as pd                    
import numpy as np                     
import matplotlib.pyplot as plt        
import seaborn as sns
import cv2

# Create your views here.
def home(request):
    return render(request, "DMFEApp/home.html")

def instructions(request):
    return render(request, "DMFEApp/instructions.html")

def eda(request):
    return render(request, "DMFEApp/eda.html")

def pca(request):
    files = models.Document.objects.all()
    return render(request, "DMFEApp/PCA.html", {"files": files})

def mostrarDatos(request, id_file):
    file = models.Document.objects.get(pk=id_file)
    archivo = pd.read_csv(file.uploadedFile)
    Correlacion = archivo.corr(method='pearson')
    archivo = archivo.to_html
    plt.figure(figsize=(14,7))
    MatrizInf = np.triu(Correlacion)
    sns.heatmap(Correlacion, cmap='RdBu_r', annot=True, mask=MatrizInf)
    plt.savefig('media/prueba3.png')
    context = {'archivo': archivo}  
    return render(request, "DMFEApp/PCA.html", context)

def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "DMFEApp/file.html", context = {
        "files": documents
    })

def listarArchivos(request):
    files = models.Document.objects.all()
    return render(request, "DMFEApp/file.html", {"files": files})

def deleteFile (request, id_file):
    file = models.Document.objects.get(pk=id_file)
    file.delete()
    files = models.Document.objects.all()
    return render(request, "DMFEApp/file.html", {"files": files})

