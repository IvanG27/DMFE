from django.shortcuts import render,HttpResponse

# Create your views here.
def  home(request):
    return render(request, "DMFEApp/home.html")

def  instructions(request):
    return render(request, "DMFEApp/instructions.html")

def  eda(request):
    return render(request, "DMFEApp/eda.html")

def  pca(request):
    return render(request, "DMFEApp/pca.html")

#def  home(request):
#    return HttpResponse("Bienvenido a DMFE")