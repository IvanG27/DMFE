from django.shortcuts import render,HttpResponse
from django.conf import settings
from . import models
from django.core.files.storage import FileSystemStorage
import pandas as pd
import pandas as pd                    
import numpy as np                     
import matplotlib.pyplot as plt        
import seaborn as sns
DatosACP = pd.DataFrame()
varPCA = 0

# Create your views here.
def home(request):
    return render(request, "DMFEApp/home.html")

def instructions(request):
    return render(request, "DMFEApp/instructions.html")

def eda(request):
    return render(request, "DMFEApp/eda.html")


##Vistas necesarias para el algotimo PCA

def pca(request):
    files = models.Document.objects.all()
    return render(request, "DMFEApp/PCA.html", {"files": files})

def mostrarDatos(request, id_file):
    file = models.Document.objects.get(pk=id_file)
    archivo = pd.read_csv(file.uploadedFile)
    
    #Obtenemos los datos de las columnas y generamos la tabla en código html
    columns = "<tr>"
    for col in archivo.columns:
        columns += f"<th>{col}</th>"
    columns += "</tr>"

    #Obtenemos los datos de las filas y generamos la tabla en código html
    rows = ""
    iter = 0
    for row in archivo.values:
        rows += "<tr>"
        for value in row:
            rows += f"<td>{value}</td>"
        rows += "</tr>"
        iter+=1
        if iter>9:
            break
    
    #Volvemos a mandar los documentos disponibles para listarlos
    files = models.Document.objects.all()

    obtenerResultadosPCA(id_file)

    #Creamos nuestro contexto
    context = {"columns": columns, "rows": rows, "files":files, "id_file": id_file}  
    return render(request, "DMFEApp/PCA.html", context)

def obtenerResultadosPCA (id_file):
    #Obtenemos el archivo que seleccionó el usuario
    file = models.Document.objects.get(pk=id_file)
    archivo = pd.read_csv(file.uploadedFile)
    Correlacion = archivo.corr(method='pearson')
    
    #Obtenemos el mapa de calor
    plt.figure(figsize=(14,7))
    MatrizInf = np.triu(Correlacion)
    sns.heatmap(Correlacion, cmap='RdBu_r', annot=True, mask=MatrizInf)
    plt.savefig('media/graficas/PCA/heatmap.png')
    plt.clf()

    #Importamos las bibliotecas necesarias
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler, MinMaxScaler

    #Estandarizamos los datos del archivo
    Estandarizar = StandardScaler()  # Se instancia el objeto StandardScaler o MinMaxScaler 
    MEstandarizada = Estandarizar.fit_transform(archivo)

    #Obtenemos el número de columnas del archivo y obtenemos los componentes
    componentes = len(archivo.columns)
    pca = PCA(componentes) #Se instancia el objeto PCA 
    pca.fit(MEstandarizada)        

    #Obtenemos la varianza
    Varianza = pca.explained_variance_ratio_
    var = 0
    componentesF = 0
    for val in Varianza:
        if var > 0.9:
            break
        componentesF += 1
        var += val

    global varPCA
    varPCA = var

    #Creamos la gráfica de la varianza acumulada
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Número de componentes')
    plt.ylabel('Varianza acumulada')
    plt.grid()
    plt.savefig('media/graficas/PCA/varianza.png')
    plt.clf()
    
    CargasComponentes = pd.DataFrame(abs(pca.components_), columns=archivo.columns)
    
    #Obtenemos las componentes principales
    z = []
    col = ''
    contadorY = 0
    for y in CargasComponentes.index:
      contador=0
      contadorX=0
      max = 0
      for x in CargasComponentes.columns:
        f = x.title()
        f = f.lower()
        valorListado = (f in z)
        if (contador == 0 and valorListado != True):
          max = CargasComponentes.iat[contadorY, contadorX]
          col = x
        elif (max < CargasComponentes.iat[contadorY, contadorX] and valorListado == False):
          max = CargasComponentes.iat[contadorY, contadorX]
          col = x
        contador += 1
        if (contador == len(CargasComponentes.columns)):
          z.append(col)
        contadorX += 1
      contadorY += 1
      if (contadorY >= componentesF-1):
        break
    
    #Eliminamos las columnas que no forman parte de las componentes principales
    DatosACP2 = archivo.drop(columns=z)
    DatosACP2 = archivo.drop(columns=DatosACP2.columns)

    print(DatosACP2.columns)

    global DatosACP
    DatosACP = DatosACP2

def  resultadosPCA(request):
    global varPCA
    varianza = varPCA
    global DatosACP
    archivo = DatosACP
    componentesP = archivo.columns
    contador = 0
    #Obtenemos los datos de las columnas y generamos la tabla en código html
    columns = "<tr>"
    for col in DatosACP.columns:
        columns += f"<th>{col}</th>"
        contador += 1
    columns += "</tr>"
    numComponentes = contador
    #Obtenemos los datos de las filas y generamos la tabla en código html
    rows = ""
    for row in DatosACP.values:
        rows += "<tr>"
        for value in row:
            rows += f"<td>{value}</td>"
        rows += "</tr>"
    
    print("Numero de componentes: " + str(numComponentes))
    print("Componentes: " + str(componentesP))
    context = {"numComponentes":numComponentes, "componentesP":componentesP, "varianza":varianza, "columns":columns, "rows": rows}
    return render(request, "DMFEApp/resultadosPCA.html", context)

#Función para subir archivos
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

##Función para listar los archivos en file.html
def listarArchivos(request):
    files = models.Document.objects.all()
    return render(request, "DMFEApp/file.html", {"files": files})

#Función para eliminar archivos subidos en file.html
def deleteFile (request, id_file):
    file = models.Document.objects.get(pk=id_file)
    file.delete()
    files = models.Document.objects.all()
    return render(request, "DMFEApp/file.html", {"files": files})

