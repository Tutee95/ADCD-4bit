# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:18:23 2017

@author: mdife
"""

#### Parametros
Trise = 5
Tfall = 5
T0 = 495
T1 = 495
von=5
NODOS = ["V_A","V_B","V_S"] #nodos entradas digitales
archivo ="test.spi"
def funcionLogica(x, von):
    """
    Aca implementas la funcion logica basada en las entradas definidas en la variable NODOS
    x es un conjunto de bits de entradas.
    Por ejemplo, si NODOS=["A0","A1","D"], x[0] es A0, x[1] es A1 y x[2] es D
    Devolver una lista con los valores de cada salida [S0, S1,...]
    Si es una sola salida, igual devolver una lista de un elemento
    """
    #Sumador
    #Poco eficiente pero mas comodo de escribir:
    vA,vB,vS=x  #hace unpack de las entradas en las variables (orden de NODOS)

    cout=vA if vS<1 else vB

    return [cout]

####
def genBits(pos, bits, von):
    length=2**bits
    pattern = 2**(bits-pos-1)
    return ([0]*pattern + [von]*pattern)* (2**pos)
def genPWL(Secuencia, nombre):
    #V1 IN 0 PWL(1 10 1n 5 1n)
    preValue = 0
    Salida = "V"+nombre + " "+nombre+" 0 PWL("
    time = 0
    for value in Secuencia:
        if value == 0:
            if preValue == 0:
                Salida = Salida + str(time + T0) + "n " + str(value) + " "
                time = time + T0
            else: #if preValue != 0:
                Salida = Salida + str(time + Tfall) + "n " + str(value) + " "
                time = time + Tfall
                Salida = Salida + str(time + T0-Tfall) + "n " + str(value) + " "
                time = time + T0-Tfall
        else: #if value != 0:
            if preValue == 0:
                Salida = Salida + str(time + Trise) + "n " + str(value) + " "
                time = time + Trise
                Salida = Salida + str(time + T1-Trise) + "n " + str(value) + " "
                time = time + T1-Trise
            else: #if preValue == 1:
                Salida = Salida + str(time + T1) + "n " + str(value) + " "
                time = time + T1
        preValue = value;
    Salida = Salida + ")"
    #print (Salida)
    return Salida
def genInputs(NODOS, von):
    salidas = []
    for n, NODO in enumerate(NODOS):
        Secuencia = genBits(n, len(NODOS), von)
        salidas.append(genPWL(Secuencia,NODO))
    return salidas

def genOutput(NODOS, von):
    secuencias=[]
    for n, NODO in enumerate(NODOS):
        secuencias.append(genBits(n, len(NODOS), von))
    entradas = zip(*secuencias)
    salidas = list(zip(*[funcionLogica(x, von) for x in entradas]))
    salidas_pwl=[]
    for n,salida in enumerate(salidas):
        salidas_pwl.append(genPWL(salida, "c_S"+str(n)))
    return salidas_pwl


entradas=genInputs(NODOS, von)

salidas_correctas=genOutput(NODOS, von)
##Generate SP
sourcelFile = open(archivo,"w")
sourcelFile.write("***** \n")
sourcelFile.write("* Generador de Signals\n")
sourcelFile.write("***** \n")
for entrada in entradas:
    sourcelFile.write(entrada)
    sourcelFile.write("\n")
for salida in salidas_correctas:
    sourcelFile.write(salida)
    sourcelFile.write("\n")
#sourcelFile.write("END;\n")
sourcelFile.close()
