import math
vientoInicial= 7 #m/s
radioRotor=63 #m
distanciaminima=315 #5*radioRotor
alturaBuje=117 #m
rugosidadSuperficial=0.694 #m
alfa= 0.0975

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
        if ma[fila][col]==1:
            arreglo.append(col)
    return arreglo

def calcularFuncionObjetivo(ma):
    potenciaTotal=0
    for fila in range(10):
        arregloPosiciones=crearArregloPorFila(fila,ma)
        for i in range(len( arregloPosiciones)):
            if i==0:
                potenciaTotal=potenciaTotal+calcularPotencia(vientoInicial)
                #print('potencia para 1')
                #print(calcularPotencia(vientoInicial))
            elif i==1:
                potenciaTotal=potenciaTotal+calcularPotencia(calcularviento(arregloPosiciones[1],arregloPosiciones[0]))
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
                potenciaTotal=potenciaTotal+calcularPotencia(viento)
                #print('potencia para 3')
                #print(calcularPotencia(viento))
    return potenciaTotal


