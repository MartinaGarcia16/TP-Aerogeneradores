import random
import codigoFuncionObjetivo
class Cromosoma():
    def __init__(self,ma):
        self.matriz=ma
        self.funcionObjetivo=codigoFuncionObjetivo.calcularFuncionObjetivo(ma)
        self.fitness=0
        self.posiciones=0

poblacionInicial=50
filas=10
columnas=10
poblacion=[]

def verificarIndices(indices,filaElegida,columnaElegida):
    ocupado=False
    for f in range(25):
        if indices[f][0]==filaElegida and indices[f][1]==columnaElegida:
            ocupado=True
    return ocupado

def verificarMolinosJuntos(ma,columnaElegida,filaElegida,i):
    molinosJuntos=False
    if columnaElegida==0:
        if ma[filaElegida][columnaElegida+1]==1:
            molinosJuntos=True
    if columnaElegida==(columnas-1):
        if ma[filaElegida][columnaElegida-1]==1:
            molinosJuntos=True
    if columnaElegida !=0 and columnaElegida !=(columnas-1):
        if ma[filaElegida][columnaElegida+1] ==1 or ma[filaElegida][columnaElegida-1]==1:
            molinosJuntos=True
    return molinosJuntos

def crearPoblacionInicial():
    #inicializar array indices
    indices = [[None for col in range(2)] for row in range(25)]

    for i in range(poblacionInicial):
        #inicializar
        ma = [[0 for col in range(10)] for row in range(10)]
        ind=0
        for dd in range(25):
            for ff in range(2):
                indices[dd][ff]=None
        cantidadMolinos=random.randint(1,25)
        for x in range(cantidadMolinos):
            aux=0
            while(aux==0):
                filaElegida= random.randint(0,filas-1)
                columnaElegida=random.randint(0,columnas-1)
            
                #comprobar que no esté en el array de indices
                ocupado = verificarIndices(indices,filaElegida,columnaElegida)
                #comprobar que no haya dos molinos juntos(teniendo en cuenta que el vento viene de izq a der)
                #Esta comprobacion se puede sacar/ preguntar al profe
                molinosJuntos = verificarMolinosJuntos(ma,columnaElegida,filaElegida,i)
                if ocupado==False and molinosJuntos==False:
                    aux=1
                    indices[ind][0]=filaElegida
                    indices[ind][1]=columnaElegida
                    ind=ind+1
                    ma[filaElegida][columnaElegida]=1
        poblacion.extend([Cromosoma(ma)])

crearPoblacionInicial()

for x in range(poblacionInicial):
    print('gen nro',x)
    for j in range(filas):
        print (poblacion[x].matriz[j])
    print(poblacion[x].funcionObjetivo)
