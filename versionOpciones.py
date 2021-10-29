import random
import math
from tkinter.constants import FALSE, TRUE
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import sys
import pygame
from pygame.locals import *
import numpy as np

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

def rellenarPoblacionInicial(cantCromosomas,poblacion1,poblacion2):

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

        poblacion1.append(matriz)
        poblacion2.append(matriz)

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
    if viento >=3 and viento <3.5:
        potencia=10
    if viento >=3.5 and viento <4:
        potencia=20
    if viento >=4 and viento <4.5:
        potencia=46
    if viento >=4.5 and viento< 5:
        potencia=110
    if viento >=5 and viento <=5.5:
        potencia=170
    if viento >=5.5 and viento <=6:
        potencia=240
    if viento >=6 and viento <=6.5:
        potencia=355
    if viento >=6.5 and viento <=7:
        potencia=460
    if viento >=7 and viento <=7.5:
        potencia=580
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
    #return potenciaTotal1

def calcularFuncion(matriz):
    total=0
    for x in range(10):
        for y in range(10):
            if matriz[x][y].HayGenerador:
                total=total+ matriz[x][y].potenciaGenerada
    return total

def FuncionObjetivoyFitness(poblacion):
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
        nuevaPoblacion.append(p1)
        nuevaPoblacion.append(p2)   
    return nuevaPoblacion

def tabla():
    generacion = np.arange(1, ciclos + 1)
    
    ######## TABLA EXCEL ########
    Datos = pd.DataFrame({"Generacion": generacion, "Minimo FO": minimos, "Maximo FO": maximos, "Promedio FO": promedios, "Minimo FO Sin Limite": minimosSinLimite, "Maximo FO Sin Limite": maximosSinLimite, "Promedio FO Sin Limite": promediosSinLimite})  
    Tabla = pd.ExcelWriter('C:\\Users\\Sergi\\Documents\\algoritmos geneticos\\Tabla.xlsx', engine='xlsxwriter') 
    Datos.to_excel(Tabla, sheet_name='Valores', index = False)     

    workbook = Tabla.book
    worksheet = Tabla.sheets["Valores"] 

    formato = workbook.add_format({"align": "center"})
    fin1="D"+str(ciclos+1)
    fin2="G"+str(ciclos+1)
    worksheet.set_column("A:D", 15, formato)
    worksheet.set_column("E:G", 25, formato)  
    worksheet.conditional_format("D1:"+fin1, {"type": "3_color_scale", "max_color": "green", "mid_color": "yellow", "min_color": "red"})
    worksheet.conditional_format("G1:"+fin2, {"type": "3_color_scale", "max_color": "green", "mid_color": "yellow", "min_color": "red"})
    Tabla.save()
#------------------------------------------------------------------------------------------------------------
def graficar(promedios,maximos,minimos,titulo):
    plt.plot(promedios,'g', label = "Promedios")
    plt.plot(maximos,'r',  label = "Maximos")
    plt.plot(minimos,'m' ,label = "Minimos")
    plt.legend(loc="lower right")
    plt.title(titulo)
    plt.show()


#----------------------------------------------------------------------------------------------------
def dibujarconpygame(poblacion,potencia,cantidad,texto,ciudad,viento,rugosidad):
    # Initialize program
    pygame.init()
    
    # Assign FPS a value
    FPS = 30
    FramePerSec = pygame.time.Clock()
    # Setting up color objects
    
    BLACK = (0, 0, 0)
    ROSA=(218,26,172)
    VERDE_CLARO = (178, 243, 99)
    VERDE_OSCURO=(60,161,23)
    # declaro la fuente que voy a utilizar.
    pygame.font.init()
    myfontTITULO = pygame.font.SysFont('Arial Black', 13)
    myfont2 = pygame.font.SysFont('Lucida Sans', 11)
    myfont = pygame.font.SysFont('Calibri', 14)
    myfontNegrita=pygame.font.SysFont('Calibri', 14)
    myfontNegrita.set_bold(True)
    # Setup a 300x300 pixel display with caption
    flags = DOUBLEBUF
    tamaño_x = 700
    tamaño_y = 700
    offset_pantalla_x = 400
    offset_pantalla_y = 0
    DISPLAYSURF =  pygame.display.set_mode((tamaño_x + offset_pantalla_x, tamaño_y + offset_pantalla_y), flags)
    DISPLAYSURF.fill(VERDE_CLARO)
    pygame.display.set_caption("TP AEROGENERADORES GRUPO 7")
    # carpeta de imagenes.
    img=[]
    img.append(pygame.image.load("img/aerogenerador.png"))
    # poniendo los molinos en las celdas
    for fila in range(10):
        for columna in range(10):
            # posicion en la pantalla
            posx = tamaño_x / 10 * columna
            posy = tamaño_y / 10 * fila
            contador=0
            if(poblacion[fila][columna].HayGenerador):
                pot= str(poblacion[fila][columna].potenciaGenerada) +" KW"
                vi=str(poblacion[fila][columna].viento)[:4]+" M/S"
                mensajepot=myfont2.render(pot,False,BLACK)
                DISPLAYSURF.blit(mensajepot, (posx+3, posy+56))
                mensajevi=myfont2.render(vi,False,BLACK)
                DISPLAYSURF.blit(mensajevi, (posx+5, posy))
                picture = pygame.transform.scale(img[0], [60, 60])
                DISPLAYSURF.blit(picture, [posx, posy+2])
                contador=contador+1
                pygame.display.flip()
                
    # dibujando celdas
    for i in range(11):
        pygame.draw.line(DISPLAYSURF, VERDE_OSCURO, (0, tamaño_y / 10 * i), (tamaño_x, tamaño_y / 10 * i), 1)
        pygame.draw.line(DISPLAYSURF, VERDE_OSCURO, (tamaño_x / 10 * i, 0), (tamaño_y / 10 * i, tamaño_y), 1)

    mensaje0=myfontTITULO.render("GRUPO 7- TP INVESTIGACION AEROGENERADORES",False,ROSA)
    DISPLAYSURF.blit(mensaje0, (715, 5))
    mensaje=myfontNegrita.render(texto,False,BLACK)
    DISPLAYSURF.blit(mensaje, (795, 45))
    mensaje6=myfontNegrita.render("CIUDAD: ",False,BLACK)
    DISPLAYSURF.blit(mensaje6, (715, 65))
    mensaje1=myfont.render(ciudad,False,BLACK)
    DISPLAYSURF.blit(mensaje1, (775, 65))
    mensaje2=myfontNegrita.render("POTENCIA GENERADA: ",False,BLACK)
    DISPLAYSURF.blit(mensaje2, (715, 85))
    mensaje2=myfont.render( str(potencia) ,False,BLACK)
    DISPLAYSURF.blit(mensaje2, (865, 85))
    mensaje2=myfont.render(" KW",False,BLACK)
    DISPLAYSURF.blit(mensaje2, (895, 85))
    mensaje3=myfontNegrita.render("VIENTO INICIAL: "  ,False,BLACK)
    DISPLAYSURF.blit(mensaje3, (715, 105))
    mensaje3=myfont.render(str(viento) ,False,BLACK)
    DISPLAYSURF.blit(mensaje3, (825, 105))
    mensaje3=myfont.render(" M/S" ,False,BLACK)
    DISPLAYSURF.blit(mensaje3, (850, 105))
    mensaje4=myfontNegrita.render("CANTIDAD AEROGENERADORES: ",False,BLACK)
    DISPLAYSURF.blit(mensaje4, (715, 125))
    mensaje4=myfont.render(str(cantidad),False,BLACK)
    DISPLAYSURF.blit(mensaje4, (930, 125))
    mensaje5=myfontNegrita.render("RUGOSIDAD DEL TERRENO: ",False,BLACK)
    DISPLAYSURF.blit(mensaje5, (715, 145))
    mensaje5=myfont.render(str(rugosidad),False,BLACK)
    DISPLAYSURF.blit(mensaje5, (895, 145))
    mensaje5=myfont.render(" M",False,BLACK)
    DISPLAYSURF.blit(mensaje5, (925, 145))
    mensaje5=myfontNegrita.render("VIENTO: ",False,BLACK)
    DISPLAYSURF.blit(mensaje5, (715, 165))
    mensaje5=myfont.render("izquerda a derecha",False,BLACK)
    DISPLAYSURF.blit(mensaje5, (775, 165))
    # Beginning Game Loop
    terminado = False
    while terminado == False:
        FramePerSec.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminado = True
        
    pygame.quit

poblacion=[]
poblacionSinLimite=[]
minimos=[]
minimosSinLimite=[]
maximos=[]
maximosSinLimite=[]
promedios=[]
promediosSinLimite=[]
cromosoma_optimo=[]
cromosoma_optimo_SinLimite=[]
max_potencia=0 #del cromosoma optimo
max_potencia_SinLimite=0
vientoInicial=0
radioRotor=45 #m
distanciaminima=225 #5*radioRotor
alturaBuje=105 #m
rugosidadSuperficial=0
alfa= 0.0975
listaFObjetivo=[]
listaFObjetivoSinLimite=[]
listaFitness=[]
listaFitnessSinLimite=[]
ciclos=100
prob_crossover=0.75
prob_mutacion=0.05
#---------------------------------------------------------------------------------------------------------------#
#print("Controlar la cantidad de aerogeneradores")
#controlar= int(input("si su respuesta es SI presione 1 de lo contrario marque 0"))
print("ingrese el numero de la ciudad elegida:")
print("1-Rufino")
print("2- Venado Tuerto")
print("3-San Jorge")
ciudad=int(input("numero: "))
if ciudad==1:
    nombreCiudad="Rufino"
    vientoInicial=6.68
    rugosidadSuperficial=0.694
if ciudad==2:
    nombreCiudad="Venado Tuerto"
    vientoInicial=6.25
    rugosidadSuperficial=2.08
if ciudad==3:
    nombreCiudad="San Jorge"
    vientoInicial=6.1
    rugosidadSuperficial=3.11

#---------------------------------------------------------------------------------------------------------------#
rellenarPoblacionInicial(50,poblacion,poblacionSinLimite)
'''print("poblacion inicial")
for x in range(50):
    print('Cromosoma: ',x+1)
    mostrarMolinos(poblacion[x])'''
for x in range(50):
        calcularPotenciasYvientos(poblacion[x])
        calcularPotenciasYvientos(poblacionSinLimite[x])

for w in range(ciclos):
    #print(w)
    listaFObjetivo,listaFitness=FuncionObjetivoyFitness(poblacion) 
    listaFObjetivoSinLimite,listaFitnessSinLimite=FuncionObjetivoyFitness(poblacionSinLimite)
    max_p=max(listaFObjetivo) #potencia de mejor cromosoma
    max_p_SinLimite=max(listaFObjetivoSinLimite)
    minimos.append(min(listaFObjetivo))
    minimosSinLimite.append(min(listaFObjetivoSinLimite))
    maximos.append(max_p)
    maximosSinLimite.append(max_p_SinLimite)
    indice = listaFObjetivo.index(max_p)
    indiceSinLimite=listaFObjetivoSinLimite.index(max_p_SinLimite)
    optimo = poblacion[indice]
    optimoSinLimite=poblacionSinLimite[indiceSinLimite]
    if w==0:
        cromosomaInicial=optimo
        potenciaInicial=max_p

    promedios.append(np.mean(listaFObjetivo))
    promediosSinLimite.append(np.mean(listaFObjetivoSinLimite))
    if (max_p > max_potencia) or (max_potencia == 0):
        max_potencia = max_p
        optimo2=optimo
    if (max_p_SinLimite > max_potencia_SinLimite) or (max_potencia_SinLimite == 0):
        max_potencia_SinLimite = max_p_SinLimite
        optimo2SinLimite=optimoSinLimite

    poblacion=crossoverYmutacion()
    poblacionSinLimite=crossoverYmutacion()

    for x in range(50):
        calcularPotenciasYvientos(poblacion[x])
        calcularPotenciasYvientos(poblacionSinLimite[x])
    #if(controlar==1):
    for j in range(50):
        cant= contar_generadores(poblacion[j])
        if (cant>25):
            poblacion[j]=corregirParque(poblacion[j],cant)


tabla()

print("mejor parque eolico inicial")
mostrarMolinos(cromosomaInicial)
print("potencia",potenciaInicial)
print(contar_generadores(cromosomaInicial))



print("mejor parque eolico")
mostrarMolinos(optimo2)
print("potencia",max_potencia)
print(contar_generadores(optimo2))

print("mejor parque eolico sin limite")
mostrarMolinos(optimo2SinLimite)
print("potencia",max_potencia_SinLimite)
print(contar_generadores(optimo2SinLimite))

dibujarconpygame(cromosomaInicial,potenciaInicial,contar_generadores(cromosomaInicial),"CROMOSOMA INICIAL",nombreCiudad,vientoInicial,rugosidadSuperficial)
dibujarconpygame(optimo2,max_potencia,contar_generadores(optimo2),"CROMOSOMA OPTIMO CON LIMITE",nombreCiudad,vientoInicial,rugosidadSuperficial)
dibujarconpygame(optimo2SinLimite,max_potencia_SinLimite,contar_generadores(optimo2SinLimite),"CROMOSOMA OPTIMO SIN LIMITE",nombreCiudad,vientoInicial,rugosidadSuperficial)
#parque = convertir_matriz(optimo2)
#print(parque)
graficar(promedios,maximos,minimos,"Grafica Con Limite")
graficar(promediosSinLimite,maximosSinLimite,minimosSinLimite,"Grafica Sin Limite")
#grafico_3d(parque)
#cuadricula(parque)
'''for x in range(50):
        print('molino: ',x+1)
        mostrarMolinos(poblacion[x])'''