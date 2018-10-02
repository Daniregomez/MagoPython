from sympy import var, solve
import numpy as np
import sympy
from math import * 
from sympy.solvers import solve


# Generar individuo de forma individual
def indGenerator(restricciones, limite_inferior, limite_superior, n, iter_desiste):


    def  S2N(elm):
        """
        Funcion que recibe un diccionario tipo {'xi0f': '-xi2f', 'xi0f': '-xi2f'}
        y lo entrega como                      {'xi0f': '-x[2]', 'xi0f': '-x[2]'}
        """
        convertido = dict()                            # Diccionario con ecuaciones en formato x[0] + x[1]
        for key, value in elm.items():

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
            convertido[''.join(str(key))] = ''.join(value)
        return convertido


    def generator(r_despejadaN, limite_inferior, limite_superior, n, iter_desiste):
        """
        Funcion que recibe las ecuaciones despejadas en terminos de cada variable, los limites, 
        cantidad de individuos requeridos y el numero de iteraciones que intentara antes de declarar que no hay convergencia o individuos que puedan 
        existir con esas ecuaciones dadas.
        Puede darse el caso de funciones con exponenciacion en la que con algunas raices no se puedan generar individuos
        """

        poblacion = list()

        # Inicializar funciones de restriccion
        if type(r_despejadaN) != type(list()):

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
                            
                    #print('_______________________________________________________________________')
                    #print(ind)


                    # CORREGIR EVALUACION DE LIMITES, testearlos todos simultaneamente y no uno por uno
                    cumple = [True] * len(limite_inferior)
                    for i in range(len(limite_inferior)):
                        # Se comprueba si: las componentes cumplen los limites de dominio, el individuo es valido
                        # Agrega el individuo a la poblacion y rompe el bucle si es True
                        if ((limite_inferior[i] > ind[i]) or (ind[i] > limite_superior[i])):
                            cumple[i] = False
                            #print(ind)
                            break

                    # BUSCAR FORMA DE RESUMIR IF 
                    if sum(cumple) == len(limite_inferior):
                        poblacion.append(list(ind))
                        break


        else:

            prim_division = n//len(r_despejadaN)


            for elm in r_despejadaN: 
                for key, value in elm.items():   
                    exec(str(key + ' = lambda x: ' + value))

                #for rang, r_despejada_elmN in zip(prim_division, r_despejadaN):
                for k in range(n//len(r_despejadaN)):

                    repeticion = 0
                    while True:                        

                        repeticion += 1
                        if repeticion == iter_desiste:
                            print('No hay convergencia')
                            break

                        # Se crea el individuo de manera aleatoria, aun no cumple restriccion
                        ind = np.random.uniform(limite_inferior, limite_superior)

                        # Se aplica la funcion restriccion y se reemplaza la evaluacion en la componente
                        # Se podria crear una poblacion mas grande para agilizar¡¡¡

                        #evaluado = [False]*len(r_despejada)

                        for key in elm.keys():   

                            # si la key es xi0f entrega 0
                            i = int(key[-2])

                            # AGREGAR MEDIDAS CONTRA ERRORES MATEMATICOS EJ: 0/0

                            # el indice i del individuo es reemplazado por la evaluacion de las otras componentes, xi1f([50.64826943 -6.58872344  5.94045401])

                            ind[i] = eval(str(key + '(ind)'))

                            #evaluado[] = True
                                


                        # CORREGIR EVALUACION DE LIMITES, testearlos todos simultaneamente y no uno por uno
                        cumple = True
                        for i in range(len(limite_inferior)):
                            # Se comprueba si: las componentes cumplen los limites de dominio, el individuo es valido
                            # Agrega el individuo a la poblacion y rompe el bucle si es True
                            if ((limite_inferior[i] >= ind[i]) or (ind[i] >= limite_superior[i])):
                                cumple = False
                                break

                        # BUSCAR FORMA DE RESUMIR IF 
                        if cumple == True:
                            poblacion.append(ind)
                            break
        
        return poblacion


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

           
    # Se colocan las variables en este formato: xi1f, xi2f, x3 = sympy.symbols('xi1f xi2f x3')
    # Se ejecuta la linea restultante para inicializarlas en forma simbolica mediante Sympi
    str1 = ''
    str2 = ''
    for var in variables:
        str1 += ',' + var
        str2 += ' ' + var

    str1 = str1[1:]
    str2 = str2[1:]

    str3 = "{} = sympy.symbols('{}')".format(str1, str2)
    exec(str3)
 

    # Se despeja cada variable en terminos de las otras y se agrega a un diccionario
    r_despejada = solve(restriccionS, variables)
    # la salida tiene formato dict si solo hay una raiz por variable, lista de dict si hay mas de una raiz por variable
    # Exa: [{xi0f: -xi2f - sqrt(201)/2 + 99/2, xi1f: 1/2 + sqrt(201)/2}, 
    #       {xi0f: -xi2f + sqrt(201)/2 + 99/2, xi1f: -sqrt(201)/2 + 1/2}]

    



    # Pasar las variables despejadas a una forma para trabajo numerico
    # Si hay raices multiples r_despejadaN sera una lista de diccionarios, de lo contrario solo un diccionario
    if type(r_despejada) == type(dict()):                  # Se comprueba si no hay raices multiples por alguna/s variable/s
        r_despejadaN = S2N(r_despejada)                    

    else:
        r_despejadaN = list()                              # Lista con ecuaciones en formato [{x[0] + x[1]}, { x[0] + x[1]}]
        for elm in r_despejada:
            r_despejada_elmN = S2N(elm)
            r_despejadaN.append(r_despejada_elmN)

    

    # CREAR POBLACION COMPLETA EN VEZ DE IND. POR IND. DESDE QUE SE CREA poblacion
    poblacion = generator(r_despejadaN, limite_inferior, limite_superior, n, iter_desiste)

    if len(poblacion) > 0:                                     # Si no se logro generar ningun individuo valido, se concluye que no se puede crear una poblacion 
                                                               # que cumpla esas restricciones

        while len(poblacion) < n:                              # Si la poblacion no esta completa, intentar una vez mas
            poblacion += generator(r_despejadaN, limite_inferior, limite_superior, n, iter_desiste)

    else:
        print("No se pueden generar individuos con las restricciones dadas")

    return poblacion[:n]


# Testeo de la funcion>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
limite_inferior = [-100, 0, -20]
limite_superior = [100, 20, 30]
n = 10
iter_desiste = 500
x1 = 'x[0] + x[1]**2 + x[2] - 100'
x2 = 'x[0] + x[1] + x[2] - 50'
#x1 = 'x[0] + x[1] + 2*x[2] - 100'
#x2 = 'x[0] + x[1] + x[2] - 50'


#f1 = (x**2) + (y**2) - 2 * (4.41 * x + 2.68 * y) + 25.59
#f2 = (x**2) + (y**2) - 2 * (3.23 * x + 2.1 * y) + 14.49
res = [x1,x2]
poblacion = indGenerator(res, limite_inferior, limite_superior, n, iter_desiste)
print(poblacion)

# Testeo de poblacion en las restricciones
x1 = lambda x: x[0] + x[1]**2 + x[2] - 100
x2 = lambda x: x[0] + x[1] + x[2] - 50
for ind in poblacion:
    print(x1(ind), x2(ind))
    

# Testeo de distribucion de elementos generados-----------------------------------
from collections import Counter

count = Counter()

for ind in poblacion:
    elm = int(ind[0])
    count[elm] += 1

print(count) 
print(sum(count.values())) 





