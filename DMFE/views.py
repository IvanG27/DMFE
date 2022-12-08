#creamos la página web
from django.http import HttpResponse

def pagina (request): #primera vista
    return HttpResponse("Primera prueba")