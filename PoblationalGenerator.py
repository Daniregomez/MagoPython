import numpy as np
import sympy
from math import * 
from sympy.solvers import solve


# Posiblemente no todas las raices esten siendo tomadas


# Generar individuo de forma individual
def indGenerator(restriccion, limite_inferior, limite_superior, n):
    # Dividir la cantidad de individuos entre la cantidad de variables, despejar la variable y evaluar
    # en la funcion que queda


    # Convertir restriccion numerica a symbolica, se remplaza x[#] por xI#F
    variables = set()                                  # Crea un conjunto donde se guardan las variables
    restriccionS = list(restriccion)                   # Restriccion en forma simbolica
    for i, c in enumerate(restriccion):                # Conversion de x[#] por xI#F
        if c == '[':

            restriccionS[i] = 'i'
            restriccionS[i + 2] = 'f'
            
            variables.add(str(restriccionS[i - 1] + restriccionS[i] + restriccionS[i + 1] + restriccionS[i + 2]))  # Se agrega la variable al conjunto

    restriccionS = ''.join(restriccionS)               


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
    exec(str3)


    # Se despeja cada variable en terminos de las otras y se agrega a un diccionario
    # var = ecn despejada en terminos de var
    r_despejada = dict()
    for var in variables:
        r_despejada[var] = solve(restriccionS, var)


    # Pasar las variables despejadas a una forma para trabajo numerico
    r_despejadaN = dict()                            # Diccionario con ecuaciones en formato x[0] + x[1]
    for key, value in r_despejada.items():

        # Se pasa el key al formato deseado
        key = list(key)
        #key[-1] = ']'
        #key[-3] = '['

        # Se pasa la ecuacion despejada al formato deseado
        value = list(str(value[0]))                         #<------------------ Arreglar----------------
        for i, c in enumerate(value):
            if c == 'i':
                value[i] = '['
                value[i + 2] = ']'

        # Se agregan los datos convertidos al formato deseado a un diccionario
        r_despejadaN[''.join(key)] = ''.join(value)


    # Se generan ind_var individuos por cada variable
    ind_var = int(n / len(variables))
    print(ind_var, n, len(variables))


    # Poblacion con n individuos
    poblacion = list()


    print(r_despejada)
    #print(r_despejadaN)


    # Se deben aprovechar todas las raices, no solo una
    # ejemplo: [-sqrt(-xi0f - xi1f - xi3f + 100), sqrt(-xi0f - xi1f - xi3f + 100)]
    # solo se toma la primera expresion
    for key, value in r_despejadaN.items():     # Se crea poblacion para cada variable

        exec(str(key + ' = lambda x: ' + value))
        i = int(key[-2])

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
                except:
                    pass
                    
                
                # Se comprueba si: las componentes cumplen los limites de dominio, el individuo es valido
                # Agrega el individuo a la poblacion y rompe el bucle si es True
                if ((limite_inferior[i] < ind[i]) and 
                    (ind[i] < limite_superior[i]) and 
                     evaluado):
                    poblacion.append(list(ind))
                    break


    return poblacion[:n]


# Testeo de la funcion
limite_inferior = [0, 0, 0, -100]
limite_superior = [10, 100, 100, 200]
n = 1000
x1 = 'x[0] + x[1] + x[2]**2 + x[3] - 100'
poblacion = indGenerator(x1, limite_inferior, limite_superior, n)
print(poblacion)


# Testeo de distribucion de elementos generados-----------------------------------
from collections import Counter

count = Counter()

for ind in poblacion:
    elm = int(ind[0])
    count[elm] += 1

print(count) 
print(sum(count.values())) 

