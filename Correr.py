import math


import matplotlib.pyplot as plt


from mago_max import mago_max
from mago_min import mago_min



# --------------------------------------------------------------------------------
# Especificaciones del problema --------------------------------------------------
# --------------------------------------------------------------------------------

limite_inferior = [-10, -10]
limite_superior = [10, 10]
n = 200
ng = 200
fObjetivo = lambda x: x[0]  + math.sin(x[1] ** 3) 

# 0 Minimiza         1 Maximiza
objetivo = 1

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


if objetivo == 0:
    resultados = mago_min(limite_inferior,limite_superior, n, ng, fObjetivo)

else:
    resultados = mago_max(limite_inferior,limite_superior, n, ng, fObjetivo)

print(resultados[0])
plt.figure()
plt.xlabel('Generacion')
plt.ylabel('Mejor individuo evaluado en fObj()')
plt.title('Generacion vs Mejor individuo evaluado en fObj()')
plt.tick_params(top='off',
                bottom='off', 
                left='off', 
                right='off')
resultados[1].plot()
plt.show()  
