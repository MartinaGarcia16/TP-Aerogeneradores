
import random
import math
vientoInicial= 7 #m/s
radioRotor=63 #m
distanciaminima=315 #5*radioRotor
alturaBuje=117 #m
rugosidadSuperficial=0.694 #m
alfa= 0.0975
listaFObjetivo=[]
listaFitness=[]
ciclos=1
prob_crossover=0.75
prob_mutacion=0.05

class Casillero():
    generador = None

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.viento = 0
        self.HayGenerador = False
        self.bin = 1 if self.HayGenerador else 0
        self.potenciaGenerada = 0
    def setPotencia(self,potencia):
        self.potenciaGenerada=potencia
    def setViento(self,viento):
        self.viento=viento
    def setHayGenerador(self,a):
        self.HayGenerador=a

def rellenarPoblacionInicial(cantCromosomas):
    poblacion = []

    for i in range(cantCromosomas):
        # creo una matriz y la relleno de casilleros en blanco.
        matriz = []
        for fila in range(10):
            renglon = []
            for columna in range(10):
                renglon.append(Casillero(fila, columna))
            matriz.append(renglon)

        # RELLENAR
        # ¿Generar menos de 25 generadores?

        cantMolinos = 0
        while cantMolinos < 25:
            numero1 = int(random.uniform(0, 10))
            numero2 = int(random.uniform(0, 10))
            casillero = matriz[numero1][numero2]
            if casillero.HayGenerador == False:
                casillero.HayGenerador = True
                cantMolinos += 1

        poblacion.append(matriz)

    return poblacion

def mostrarMolinos(matriz):
    print("molinos")
    for fila in range(10):
        print("")
        for columna in range(10):
            if(matriz[fila][columna].HayGenerador):
                print("[ X ]", end="")
            else:
                print("[   ]", end="")
    print()

def calcularPotencia(viento):
    potencia=0
    if viento >=3 and viento <5:
        potencia=35
    if viento >=5 and viento <8:
        potencia=404
    if viento >=8 and viento <10:
        potencia=1760
    if viento >=10 and viento< 13:
        potencia=3187
    if viento >=13 and viento <=22:
        potencia=3450
    return potencia

def calcularviento(posFinal,posini):
    r1=radioRotor+alfa*((posFinal-posini)*distanciaminima)
    viento= vientoInicial*(1-((2/3)*((radioRotor/r1)**2)))
    return viento

def crearArregloPorFila(fila,ma):
    arreglo=[]
    for col in range(10):
        if ma[fila][col].HayGenerador:
            arreglo.append(col)
    return arreglo

def calcularPotenciasYvientos(ma):
    #potenciaTotal=0
    for fila in range(10):
        arregloPosiciones=crearArregloPorFila(fila,ma)
        for i in range(len( arregloPosiciones)):
            if i==0:
                #potenciaTotal=potenciaTotal+calcularPotencia(vientoInicial)
                ma[fila][arregloPosiciones[i]].setViento(vientoInicial)
                ma[fila][arregloPosiciones[i]].setPotencia(calcularPotencia(vientoInicial))
                #print('potencia para 1')
                #print(calcularPotencia(vientoInicial))
            elif i==1:
                #potenciaTotal=potenciaTotal+calcularPotencia(calcularviento(arregloPosiciones[1],arregloPosiciones[0]))
                viento=calcularviento(arregloPosiciones[1],arregloPosiciones[0])
                ma[fila][arregloPosiciones[i]].setViento(viento)
                ma[fila][arregloPosiciones[i]].setPotencia(calcularPotencia(viento))
                #ma[fila][arregloPosiciones[i]].setPotencia(calcularPotencia(calcularviento(arregloPosiciones[1],arregloPosiciones[0])))
                #print('viento para 2')
                #print(calcularviento(arregloPosiciones[1],arregloPosiciones[0]))
                #print('potencia para 2')
                #print(calcularPotencia(calcularviento(arregloPosiciones[1],arregloPosiciones[0])))
            else:
                total=0
                viento=0
                for j in range(i):
                    total=total+(1-(calcularviento(arregloPosiciones[i],arregloPosiciones[j])/vientoInicial))**2
                viento=vientoInicial*( 1- math.sqrt(total))
                #print('viento para 3')
                #print(viento)
                #potenciaTotal=potenciaTotal+calcularPotencia(viento)
                ma[fila][arregloPosiciones[i]].setViento(viento)
                ma[fila][arregloPosiciones[i]].setPotencia(calcularPotencia(viento))
                #print('potencia para 3')
                #print(calcularPotencia(viento))
    #return potenciaTotal

def calcularFuncion(matriz):
    total=0
    for x in range(10):
        for y in range(10):
            if matriz[x][y].HayGenerador:
                total=total+ matriz[x][y].potenciaGenerada
    return total

def FuncionObjetivoyFitness(pobacion):
    listaFuncion=[]
    listaFitness=[]
    for x in range(50):
        listaFuncion.append(calcularFuncion(poblacion[x]))
    sumaTotal=sum(listaFuncion)
    for y in range(50):
        listaFitness.append((listaFuncion[y])/sumaTotal)
    return listaFuncion,listaFitness     

def crearRuleta(listaFitness):
    ruleta=[]
    for x in range(50):
        aux=int(round(listaFitness[x]*1000))
        for _ in range(0,aux):
            ruleta.append(x)
    #print('ruleta')
    #print(ruleta)
    return ruleta

def crossover(p1,p2):
    #inicializo hijo1
    hijo1 = []
    for fila in range(10):
            renglon = []
            for columna in range(10):
                renglon.append(Casillero(fila, columna))
            hijo1.append(renglon)
    #inicializo hijo 2
    hijo2 = []
    for fila in range(10):
            renglon = []
            for columna in range(10):
                renglon.append(Casillero(fila, columna))
            hijo2.append(renglon)

    if(random.random() <= prob_crossover):
        # primer hijo sale por mejores filas.
        for f in range(10):
            puntajeFila1 = 0
            puntajeFila2 = 0
            for c in range(10):
                if(p1[f][c].HayGenerador):
                    puntajeFila1 += p1[f][c].potenciaGenerada
                if(p2[f][c].HayGenerador):
                    puntajeFila2 += p2[f][c].potenciaGenerada
            if(puntajeFila1 >= puntajeFila2):
                for z in range(10):
                    if (p1[f][z].HayGenerador):
                        hijo1[f][z].setHayGenerador(True)
            else:
                for z in range(10):
                    if (p2[f][z].HayGenerador):
                        hijo1[f][z].setHayGenerador(True)

        # segundo hijo sale por mejores columnas

        for c in range(10):
            puntajeColumna1 = 0
            puntajeColumna2 = 0
            for f in range(10):
                if(p1[f][c].HayGenerador):
                    puntajeColumna1 += p1[f][c].potenciaGenerada
                if(p2[f][c].HayGenerador):
                    puntajeColumna2 += p2[f][c].potenciaGenerada

            if (puntajeColumna1 >= puntajeColumna2):
                for f in range(10):
                    if p1[f][c].HayGenerador:
                        hijo2[f][c].setHayGenerador(True)
            else:
                for f in range(10):
                    if p2[f][c].HayGenerador:
                        hijo2[f][c].setHayGenerador(True)
    print('hijo 1')
    for fila in range(10):
        print("")
        for columna in range(10):
            if(hijo1[fila][columna].HayGenerador):
                print("[ X ]", end="")
            else:
                print("[   ]", end="")
    print('hijo2')              
    for fila in range(10):
        print("")
        for columna in range(10):
            if(hijo2[fila][columna].HayGenerador):
                print("[ X ]", end="")
            else:
                print("[   ]", end="")
    return hijo1, hijo2
def mutacion(padre):
    fila=random.randint(0,9)
    columna=random.randint(0,9)
    if padre[fila][columna].HayGenerador:
        padre[fila][columna].setHayGenerador(False)
    else:
        padre[fila][columna].setHayGenerador(True)
    return padre

def crossoverYmutacion():
    nuevaPoblacion=[]
    ruleta=crearRuleta(listaFitness)
    for _ in range(0,int(len(poblacion)/2)):
        p1 =poblacion[ random.choice(ruleta)]
        p2 = poblacion[random.choice(ruleta)]
        p1,p2= crossover(p1,p2)
        p1=mutacion(p1)
        p2=mutacion(p2)
        nuevaPoblacion.append(p1)
        nuevaPoblacion.append(p2)   
    return nuevaPoblacion
#------------------------------------------------------------------------------------------------------------
poblacion=rellenarPoblacionInicial(50)
print("poblacion inicial")
for x in range(50):
    print('molino: ',x+1)
    mostrarMolinos(poblacion[x])

for _ in range(ciclos):

    for x in range(50):
        calcularPotenciasYvientos(poblacion[x])

    listaFObjetivo,listaFitness=FuncionObjetivoyFitness(poblacion)  

    print('funcion ojetivo')
    print(listaFObjetivo)
    print('fitness')
    print(listaFitness)

    poblacion=crossoverYmutacion()

    for x in range(50):
        print('molino: ',x+1)
        mostrarMolinos(poblacion[x])

    

    

    