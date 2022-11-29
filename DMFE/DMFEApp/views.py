from django.shortcuts import render,HttpResponse
from django.conf import settings
from . import models
from django.core.files.storage import FileSystemStorage

# Create your views here.
def  home(request):
    return render(request, "DMFEApp/home.html")

def  instructions(request):
    return render(request, "DMFEApp/instructions.html")

def  eda(request):
    return render(request, "DMFEApp/eda.html")

def  pca(request):
    return render(request, "DMFEApp/pca.html")

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

    return render(request, "DMFEApp/pca.html", context = {
        "files": documents
    })