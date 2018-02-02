from functools import reduce

import numpy as np
import pandas as pd


def mago_max(lmt_inferior, lmt_superior, n, ng, fObjetivo):

    # Generacion de la poblacion inicial
    poblacion = generarPoblacion(lmt_inferior,lmt_superior, n)


    # Serie donde se guarda el mejor valor de fobj de cada generacion, para fines ilustrativos
    best_fobj = pd.Series()


    # Lista donde se guardan todos los datos que seran regresados por la funcion
    datos = list()


    for i in range(ng):

        print('Generacion numero: ', i + 1)

        # Evaluar poblacion en fobj
        resultados = evaluarPoblacion(poblacion, fObjetivo)


        # Se agrega el mejor individuo de la generacion a best_fobj
        best_fobj = best_fobj.append(pd.Series({i + 1 : resultados.index[-1]}))


        # Calculos estadisticos varios
        s = np.cov(poblacion, rowvar=False)
        sd = np.sqrt(np.diag(s))   
        media = np.mean(poblacion, axis=0)           
                
        mini = np.subtract(media, np.multiply(0.5, sd) )
        maxi = np.add(media, np.multiply(0.5, sd) )
        
        mini1 = np.subtract(media,  sd)
        maxi1 = np.add(media,  sd)


        # Calculo de las cardinalidades
        poblacionRegion_1 = filtrarIndividuosRegion(poblacion, mini, maxi)
        poblacionRegion_2 = filtrarIndividuosRegion(poblacion, mini1, maxi1)


        n1= sum(poblacionRegion_1)           
        if n1 < 0:
            n1 = 0

        n2 = sum(poblacionRegion_2) - n1 - 1
        if n2 < 0:
            n2 = 0

        n3 = n - n1 - n2

        sn = np.multiply(s, 1/np.linalg.norm(s,np.inf))


        # Si hay individuos en n1, calcular diferencias y hacerlos competir
        if n1 > 0:
            resultados = competenciaG1(resultados, n1, sn, fObjetivo, lmt_inferior, lmt_superior)
            grupo_mejores = resultados.iloc[-n1: ] 


        # Poblacion de la siguiente generacion
        poblacion = list()

        if n1 != 0:
            poblacion.extend(grupo_mejores)
        else:
            # En caso de que n1 sea 0, guarda el mejor individuo para la proxima generacion
            # y resta 1 a n3 o n1 para mantener la poblacion en n individuos
            poblacion.append(resultados.iat[-1])
            if n3 != 0:
                n3 -= 1
            else:
                n2 -=1

        if n2 != 0:
            poblacion.extend(generarPoblacion(mini, maxi, n2))

        if n3 != 0:
            poblacion.extend(generarPoblacion(lmt_inferior, lmt_superior, n3))


    datos.append("\nResultado:\n{} \n\nFuncion objetivo:\n{}\n ".format(resultados.iat[-1], resultados.index[-1]))
    datos.append(best_fobj)


    return datos


def generarPoblacion(limite_inferior, limite_superior, n):
    """
    Genera poblacion de manera uniforme, 
    primero una columna para cada variable de largo n, cada poblacion se 
    encuentra entre el lmt_superior y lmt_inferior de la variable respectiva
    despues transpone y entrega un vector de tuplas donde cada 1 es un individuo
    """
    pob = zip(*[np.random.uniform(limite_inferior[i] ,limite_superior[i] , n) for i in range(len(limite_inferior))])

    return [ind for ind in pob]


def evaluarPoblacion(poblacion, fObjetivo):
    """
    Evalua la poblacion, despues genera una serie con index = f(ind) y el respectivo individuo
    """

    resultados = dict()
    
    for i in poblacion:
        resultados[fObjetivo(i)] = i

    resultados = pd.Series(resultados)

    return resultados


def filtrarIndividuosRegion(resultados, limite_inferior, limite_superior):
    """
    Filtra los individuos segun limites inferiores y superiores y entrega una boolean mask
    """
        
    variableCumple = lambda x,li,ls: x>=li and x<=ls
    reducirCondicion = lambda x,y: x and y    

    individuosRegion=[]  

    for ind in resultados:

        val =  map(variableCumple,ind,limite_inferior, limite_superior) 
        individuosRegion.append(reduce(reducirCondicion, val))

    return individuosRegion


def competenciaG1(resultados, n1, sn, fobj, lim_inf, lim_sup):
    """
    Selecciona el grupo de los mejores individuos (cardinalidad n1) y los hace competir con una version
    alterada de si mismos segun la formula 2 y 3 de la documentacion, en caso de que sea mejor se borra
    el original y se agrega a la nueva version
    """

    lng_pob = len(resultados)
    lng_lim = len(lim_inf)

    grupo_mejores = resultados.iloc[-n1: ] 
    mejorIndividuo = resultados.iat[-1]
   
    for ind in grupo_mejores:

        xb = np.array(mejorIndividuo)
        b = np.random.randint(0, lng_pob)
        xm = np.array(resultados.iat[b])
        xt = ind + sn.dot(xb - xm)

        for i in range(lng_lim):
            if xt[i] < lim_inf[i]:
                xt[i] = lim_inf[i]
            if xt[i] > lim_sup[i]:
                xt[i] = lim_sup[i]

        if fobj(xt) > fobj(ind):

            resultados = (resultados.drop([fobj(ind)])
                                    .append(pd.Series({fobj(xt):xt})))

    resultados.sort_index(inplace=True)
    
    return resultados
