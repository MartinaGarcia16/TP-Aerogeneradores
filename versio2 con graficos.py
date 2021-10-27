import random
import math
from tkinter.constants import FALSE, TRUE
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import sys
import pygame
from pygame.locals import KEYDOWN, K_q
import numpy as np


vientoInicial= 7 #m/s
radioRotor=63 #m
distanciaminima=315 #5*radioRotor
alturaBuje=117 #m
rugosidadSuperficial=0.694 #m
alfa= 0.0975
listaFObjetivo=[]
listaFitness=[]
ciclos=50
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
    def getBin():
        return bin

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
    else: 
        hijo1=p1
        hijo2=p2
    '''print('hijo 1')
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
                print("[   ]", end="")'''
    return hijo1, hijo2

def mutacion(padre):
    if(random.random() <= prob_crossover):
        fila=random.randint(0,9)
        columna=random.randint(0,9)
        if padre[fila][columna].HayGenerador:
            padre[fila][columna].setHayGenerador(False)
        else:
            padre[fila][columna].setHayGenerador(True)
    return padre

def contar_generadores(parque):
    nro_generadores = 0
    for i in range(10):
        for j in range(10):
            if parque[i][j].HayGenerador:
                nro_generadores += 1
    return nro_generadores

def corregirParque(parque, cant_generadores_parque):
    
    nro_generadores_a_borrar = cant_generadores_parque - 25
    aux=0
    while(aux<nro_generadores_a_borrar):
        fila=random.randint(0,9)
        columna=random.randint(0,9)
        if parque[fila][columna].HayGenerador and parque[fila][columna].potenciaGenerada <=404:
            parque[fila][columna].setHayGenerador(False)
            aux=aux+1
    return parque

def crossoverYmutacion():
    nuevaPoblacion=[]
    ruleta=crearRuleta(listaFitness)
    for _ in range(0,int(len(poblacion)/2)):
        p1 =poblacion[ random.choice(ruleta)]
        p2 = poblacion[random.choice(ruleta)]
        p1,p2= crossover(p1,p2)
        p1=mutacion(p1)
        p2=mutacion(p2)
        '''cant1=contar_generadores(p1)
        cant2=contar_generadores(p2)
        if cant1>25:
           p1= corregirParque(p1,cant1)
        if cant2>25:
            p2=corregirParque(p2,cant2)'''

        nuevaPoblacion.append(p1)
        nuevaPoblacion.append(p2)   
    return nuevaPoblacion

def tabla():
    generacion = np.arange(1, ciclos + 1)
    
    ######## TABLA EXCEL ########
    Datos = pd.DataFrame({"Generacion": generacion, "Minimo FO": minimos, "Maximo FO": maximos, "Promedio FO": promedios})  
    Tabla = pd.ExcelWriter('C:\\Users\\Usuario\\Desktop\\Tabla.xlsx', engine='xlsxwriter') 
    Datos.to_excel(Tabla, sheet_name='Valores', index = False)     

    workbook = Tabla.book
    worksheet = Tabla.sheets["Valores"] 

    formato = workbook.add_format({"align": "center"})

    worksheet.set_column("A:D", 15, formato)  
    worksheet.conditional_format("D1:DF"+str(len(promedios)+1), {"type": "3_color_scale", "max_color": "green", "mid_color": "yellow", "min_color": "red"})

    Tabla.save()
#------------------------------------------------------------------------------------------------------------
def convertir_matriz(ma):
    ma2=np.zeros((10, 10))
    for fila in range(10):
        for columna in range(10):
            if(ma[fila][columna].HayGenerador):
                ma2[fila][columna]=1
            else:
                ma2[fila][columna]=0
    return ma2

def grafico_3d(ma):
    x=[]
    y=[]
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    for i in range(10):
        for j in range(10):
            if ma[i][j] == 1:
                print("x",i)
                print("y",j)
                x.append(i)
                y.append(j)
    print(x)
    print(y)
    # Definimos los datos
    z3 = np.zeros(25)

    dx = np.ones(25)
    dy = np.ones(25)
    dz = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

    # utilizamos el método bar3d para graficar las barras
    ax1.bar3d(x, y, z3, dx, dy, dz)

    # Mostramos el gráfico
    plt.show()

def cuadricula(ma):
    # CONSTANTS:
    SCREENSIZE = WIDTH, HEIGHT = 800, 600
    BLACK = (0, 0, 0)
    GREY = (160, 160, 160)

    # OUR GRID MAP:
    cellMAP = ma

    _VARS = {'surf': False, 'gridWH': 400,
            'gridOrigin': (200, 100), 'gridCells': cellMAP.shape[0], 'lineWidth': 2}


    def main():
        pygame.init()
        _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
        while True:
            checkEvents()
            _VARS['surf'].fill(GREY)
            drawSquareGrid(
            _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
            placeCells()
            pygame.display.update()


    # NEW METHOD FOR ADDING CELLS :
    def placeCells():
        # GET CELL DIMENSIONS...
        cellBorder = 6
        celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
        # DOUBLE LOOP
        for row in range(cellMAP.shape[0]):
            for column in range(cellMAP.shape[1]):
                # Is the grid cell tiled ?
                if(cellMAP[column][row] == 1):
                    drawSquareCell(
                        _VARS['gridOrigin'][0] + (celldimY*row)
                        + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                        _VARS['gridOrigin'][1] + (celldimX*column)
                        + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                        celldimX, celldimY)

    # Draw filled rectangle at coordinates
    def drawSquareCell(x, y, dimX, dimY):
        pygame.draw.rect(
        _VARS['surf'], BLACK,
        (x, y, dimX, dimY)
        )


    def drawSquareGrid(origin, gridWH, cells):

        CONTAINER_WIDTH_HEIGHT = gridWH
        cont_x, cont_y = origin

        # DRAW Grid Border:
        # TOP lEFT TO RIGHT
        pygame.draw.line(
        _VARS['surf'], BLACK,
        (cont_x, cont_y),
        (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), _VARS['lineWidth'])
        # # BOTTOM lEFT TO RIGHT
        pygame.draw.line(
        _VARS['surf'], BLACK,
        (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
        (CONTAINER_WIDTH_HEIGHT + cont_x,
        CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])
        # # LEFT TOP TO BOTTOM
        pygame.draw.line(
        _VARS['surf'], BLACK,
        (cont_x, cont_y),
        (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), _VARS['lineWidth'])
        # # RIGHT TOP TO BOTTOM
        pygame.draw.line(
        _VARS['surf'], BLACK,
        (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
        (CONTAINER_WIDTH_HEIGHT + cont_x,
        CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])

        # Get cell size, just one since its a square grid.
        cellSize = CONTAINER_WIDTH_HEIGHT/cells

        # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
        for x in range(cells):
            pygame.draw.line(
            _VARS['surf'], BLACK,
            (cont_x + (cellSize * x), cont_y),
            (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
        # # HORIZONTAl DIVISIONS
            pygame.draw.line(
            _VARS['surf'], BLACK,
            (cont_x, cont_y + (cellSize*x)),
            (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)


    def checkEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()


    if __name__ == '__main__':
        main()

minimos=[]
maximos=[]
promedios=[]
cromosoma_optimo=[]
max_potencia=0 #del cromosoma optimo

poblacion=rellenarPoblacionInicial(50)
'''print("poblacion inicial")
for x in range(50):
    print('Cromosoma: ',x+1)
    mostrarMolinos(poblacion[x])'''
for x in range(50):
        calcularPotenciasYvientos(poblacion[x])

for w in range(ciclos):
    #print(w)
    listaFObjetivo,listaFitness=FuncionObjetivoyFitness(poblacion) 
    max_p=max(listaFObjetivo) #potencia de mejor cromosoma
    minimos.append(min(listaFObjetivo))
    maximos.append(max_p)
    indice = listaFObjetivo.index(max_p)
    optimo = poblacion[indice]
    promedios.append(np.mean(listaFObjetivo))
    if (max_p > max_potencia) or (max_potencia == 0):
        max_potencia = max_p
        optimo2=optimo

    poblacion=crossoverYmutacion()
    for x in range(50):
        calcularPotenciasYvientos(poblacion[x])
    for j in range(50):
        cant= contar_generadores(poblacion[j])
        if (cant>25):
            poblacion[j]=corregirParque(poblacion[j],cant)


tabla()
print("mejor parque eolico")
mostrarMolinos(optimo2)
print("potencia",max_potencia)
print(contar_generadores(optimo2))

parque = convertir_matriz(optimo2)
print(parque)
grafico_3d(parque)
cuadricula(parque)
'''for x in range(50):
        print('molino: ',x+1)
        mostrarMolinos(poblacion[x])'''