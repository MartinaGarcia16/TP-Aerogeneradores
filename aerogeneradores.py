import random
import codigoFuncionObjetivo
class Cromosoma():
    def __init__(self,ma):
        self.matriz=ma
        self.funcionObjetivo=codigoFuncionObjetivo.calcularFuncionObjetivo(ma)
        self.fitness=0
        self.posiciones=0
    def setFitness(self, fitness):
        self.fitness=fitness
    def setPosiciones(self,posiciones):
        self.posiciones=posiciones

poblacionInicial=50
filas=10
columnas=10
poblacion=[]
cilos=3
prob_crossover=0.75
prob_mutacion=0.05

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
        cantidadMolinos=25 #random.randint(1,25)
        for x in range(cantidadMolinos):
            aux=0
            while(aux==0):
                filaElegida= random.randint(0,filas-1)
                columnaElegida=random.randint(0,columnas-1)
            
                #comprobar que no esté en el array de indices
                ocupado = verificarIndices(indices,filaElegida,columnaElegida)
                #comprobar que no haya dos molinos juntos(teniendo en cuenta que el vento viene de izq a der)
                #preguntar si esta comprobacion es necesaria
                #molinosJuntos = verificarMolinosJuntos(ma,columnaElegida,filaElegida,i)
                if ocupado==False: #and molinosJuntos==False:
                    aux=1
                    indices[ind][0]=filaElegida
                    indices[ind][1]=columnaElegida
                    ind=ind+1
                    ma[filaElegida][columnaElegida]=1
        poblacion.extend([Cromosoma(ma)])

def calcularFitnessYPosiciones(poblacion):
    total=0.0
    for x in range(len(poblacion)):
        total=total+poblacion[x].funcionObjetivo
    for x in range(len(poblacion)):
        poblacion[x].setFitness(poblacion[x].funcionObjetivo/total)
        poblacion[x].setPosiciones(int(round(1000*poblacion[x].fitness)))

def crossover(poblacion):
    ruleta=crearRuleta(poblacion)
    hijos=[]
    for _ in range(0,int(len(poblacion)/2)):
        padre_1 = random.choice(ruleta)
        padre_2 = random.choice(ruleta)
        #cruce
        if (random.random() <= prob_crossover):
            print('cruce')
        #mutacion (elegir al azar una posicion: si hay un 0 se cambia por 1 y viceversa)
        if (random.random() <= prob_mutacion):
            padre_1=hacerMutacion(padre_1)
        if (random.random() <= prob_mutacion):
            padre_2=hacerMutacion(padre_2)
        #hijos.extend([Cromosoma(padre_1),Cromosoma(padre_2)])
    #return hijos

def crearRuleta(poblacion):
    ruleta=[]
    for x in range(len(poblacion)):
        aux=poblacion[x].posiciones
        for _ in range(0,aux):
            ruleta.extend([poblacion[x].matriz])
    return ruleta

def hacerMutacion(padre):
    fila=random.randint(0,len(padre)-1)
    columna=random.randint(0,len(padre)-1)
    if padre[fila][columna]==0:
        padre[fila][columna]=1
    else:
        padre[fila][columna]=0
    return padre
#programa principal
crearPoblacionInicial()
calcularFitnessYPosiciones(poblacion)
crossover(poblacion)

'''
for x in range(poblacionInicial):
    print('gen nro',x)
    for j in range(filas):
        print (poblacion[x].matriz[j])
    print(poblacion[x].funcionObjetivo)
    print(poblacion[x].fitness)
    print(poblacion[x].posiciones)'''
