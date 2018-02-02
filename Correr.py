import matplotlib.pyplot as plt


from mago_max import mago_max
from mago_min import mago_min


# --------------------------------------------------------------------------------
# Especificaciones del problema --------------------------------------------------
# --------------------------------------------------------------------------------

limite_inferior = [-10, -10, -10, -10, -30]
limite_superior = [10, 10, 10, 10, 30]
n = 50
ng = 200
fObjetivo = lambda x: sum(x)

# 0 Minimiza         1 Maximiza
objetivo = 0

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


if objetivo == 0:
    datos = mago_min(limite_inferior,limite_superior, n, ng, fObjetivo)

else:
    datos = mago_max(limite_inferior,limite_superior, n, ng, fObjetivo)

print(datos[0])
plt.figure()
plt.xlabel('Generacion')
plt.ylabel('Mejor individuo evaluado en fObj()')
plt.title('Generacion vs Mejor individuo evaluado en fObj()')
plt.tick_params(top='off',
                bottom='off', 
                left='off', 
                right='off')
datos[1].plot()
plt.show()  
