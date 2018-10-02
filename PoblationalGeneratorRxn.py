from sympy import var, solve
import numpy as np
import sympy
from math import * 
from sympy.solvers import solve

# Codigo para Rn restricciones de igualdad



#x, y = var('x y')



#sols = solve((f1, f2), (x, y))








# Generar individuo de forma individual
def indGenerator(restricciones, limite_inferior, limite_superior, n):
    # Dividir la cantidad de individuos entre la cantidad de variables, despejar la variable y evaluar
    # en la funcion que queda

    variables = set()                                  # Crea un conjunto donde se guardan las variables
    restriccionS = restricciones                       # Restriccion en forma simbolica

    for i ,R in enumerate(restricciones):              # indice, restriccion
        restriccionS[i] = list(R)                      # convierte la restriccion i en una lista

        for j, c in enumerate(R):                      # Conversion de x[#] por xI#F
            if c == '[':
                restriccionS[i][j] = 'i'
                restriccionS[i][j + 2] = 'f'

                variables.add(''.join(restricciones[i][j - 1: j + 3]))  # Se agrega la variable al conjunto

        restriccionS[i] = ''.join(restriccionS[i])     # Se convierte la restriccion en forma de lista en un str

    print(restriccionS, variables)
           


    # Se colocan las variables en este formato: xi1f, xi2f, x3 = sympy.symbols('xi1f xi2f x3')
    # Se ejecuta la linea restultante para inicializarlas en forma simbolica mediante Sympi
    str1 = ''
    str2 = ''
    for var in variables:
        str1 += ',' + var
        str2 += ' ' + var

    str1 = str1[1:]
    str2 = str2[1:]

    str3 = str1 + " = sympy.symbols('" + str2 + "')"
    #print(str3)
    exec(str3)



    # Se despeja cada variable en terminos de las otras y se agrega a un diccionario
    r_despejada = solve(restriccionS, variables)
    print('___________________')
    #print(variables)
    #print(restriccionS)
    print(r_despejada)
    print('___________________')


    # Pasar las variables despejadas a una forma para trabajo numerico
    r_despejadaN = dict()                            # Diccionario con ecuaciones en formato x[0] + x[1]
    for key, value in r_despejada.items():
        #print('\n',value)

        # Se pasa el key al formato deseado
        #key = list(key)
        #key[-1] = ']'
        #key[-3] = '['
        

        # Se pasa la ecuacion despejada al formato deseado
        value = list(str(value))                         #<------------------ Arreglar----------------
        for i, c in enumerate(value):
            if c == 'i':
                value[i] = '['
                value[i + 2] = ']'

        # Se agregan los datos convertidos al formato deseado a un diccionario
        r_despejadaN[''.join(str(key))] = ''.join(value)

    #print(r_despejadaN)

        
    #  ----------------------------------------voy aqui
    # NO TODAS LAS POSIBLES RAICES ESTAN SIENDO TOMADAS¡¡¡¡¡
    # CREAR POBLACION COMPLETA EN VEZ DE IND. POR IND. DESDE QUE SE CREA poblacion
    # Variante de for anterior
    poblacion = list()


    # Inicializar funciones de restriccion
    for key, value in r_despejadaN.items():   

        exec(str(key + ' = lambda x: ' + value))



    for k in range(n):
        repeticion = 0
        while True:                        

            repeticion += 1
            if repeticion == 100:
                print('No hay convergencia')
                break

            # Se crea el individuo de manera aleatoria, aun no cumple restriccion
            ind = np.random.uniform(limite_inferior, limite_superior)

            # Se aplica la funcion restriccion y se reemplaza la evaluacion en la componente
            # Se podria crear una poblacion mas grande para agilizar¡¡¡

            #evaluado = [False]*len(r_despejada)

            for key in r_despejadaN.keys():   

                i = int(key[-2])

                # AGREGAR MEDIDAS CONTRA ERRORES MATEMATICOS EJ: 0/0
                
                ind[i] = eval(str(key + '(ind)'))

                #evaluado[] = True
                    
            print('_______________________________________________________________________')
            #print(ind)


            # CORREGIR EVALUACION DE LIMITES, testearlos todos simultaneamente y no uno por uno
            cumple = [True] * len(limite_inferior)
            for i in range(len(limite_inferior)):
                # Se comprueba si: las componentes cumplen los limites de dominio, el individuo es valido
                # Agrega el individuo a la poblacion y rompe el bucle si es True
                if ((limite_inferior[i] > ind[i]) or (ind[i] > limite_superior[i])):
                    cumple[i] = False
                    print(ind)
                    break

            # BUSCAR FORMA DE RESUMIR IF 
            if sum(cumple) == len(limite_inferior):
                poblacion.append(list(ind))
                break



    """
    for key, value in r_despejadaN.items():     

        exec(str(key + ' = lambda x: ' + value))
        i = int(key[-2])

        print(key, value)
        print(str(key + ' = lambda x: ' + value))

        #for index ,ind in enumerate(poblacion):               # Se crean ind_var individuos
        for k in range(n):
            repeticion = 0
            while True:                        

                repeticion += 1
                if repeticion == 100:
                    print('No hay convergencia')
                    break

                # Se crea el individuo de manera aleatoria, aun no cumple restriccion
                ind = np.random.uniform(limite_inferior, limite_superior)

                # Se aplica la funcion restriccion y se reemplaza la evaluacion en la componente
                # Se podria crear una poblacion mas grande para agilizar¡¡¡

                evaluado = False

                try:
                    ind[i] = eval(str(key + '(ind)'))
                    evaluado = True
                    print(ind)
                except:
                    pass
                    
                
                # Se comprueba si: las componentes cumplen los limites de dominio, el individuo es valido
                # Agrega el individuo a la poblacion y rompe el bucle si es True
                if ((limite_inferior[i] < ind[i]) and 
                    (ind[i] < limite_superior[i]) and 
                     evaluado):
                    poblacion.append(list(ind))
                    print(ind)
                    break
    """


    # Se deben aprovechar todas las raices, no solo una
    # ejemplo: [-sqrt(-xi0f - xi1f - xi3f + 100), sqrt(-xi0f - xi1f - xi3f + 100)]
    # solo se toma la primera expresion
    """
    for key, value in r_despejadaN.items():     # Se crea poblacion para cada variable

        exec(str(key + ' = lambda x: ' + value))
        i = int(key[-2])

        print(key, value)
        print(str(key + ' = lambda x: ' + value))

        for k in range(ind_var):               # Se crean ind_var individuos
            repeticion = 0
            while True:                        # Se crea individuo

                repeticion += 1
                if repeticion == 100:
                    print('No hay convergencia')
                    break

                # Se crea el individuo de manera aleatoria, aun no cumple restriccion
                ind = np.random.uniform(limite_inferior, limite_superior)

                # Se aplica la funcion restriccion y se reemplaza la evaluacion en la componente
                # Se podria crear una poblacion mas grande para agilizar¡¡¡

                evaluado = False

                try:
                    ind[i] = eval(str(key + '(ind)'))
                    evaluado = True
                    print(ind)
                except:
                    pass
                    
                
                # Se comprueba si: las componentes cumplen los limites de dominio, el individuo es valido
                # Agrega el individuo a la poblacion y rompe el bucle si es True
                if ((limite_inferior[i] < ind[i]) and 
                    (ind[i] < limite_superior[i]) and 
                     evaluado):
                    poblacion.append(list(ind))
                    print(ind)
                    break
    """

    return poblacion[:n]


# Testeo de la funcion
limite_inferior = [0, 100, -200, 300]
limite_superior = [100, 200, 300, 400]
n = 100
x1 = 'x[0] + x[1] + x[2] - 100'
x2 = 'x[0] + x[1] + 2*x[2] - 50'

#f1 = (x**2) + (y**2) - 2 * (4.41 * x + 2.68 * y) + 25.59
#f2 = (x**2) + (y**2) - 2 * (3.23 * x + 2.1 * y) + 14.49
res = [x1,x2]
poblacion = indGenerator(res, limite_inferior, limite_superior, n)
print(poblacion)


# Testeo de distribucion de elementos generados-----------------------------------
from collections import Counter

count = Counter()

for ind in poblacion:
    elm = int(ind[0])
    count[elm] += 1

print(count) 
print(sum(count.values())) 





