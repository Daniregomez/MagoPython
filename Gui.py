from sys import exit, argv, modules
from os import getenv
from re import findall, sub

from numpy import cov, sqrt, mean, subtract, add, diag, multiply, linalg, inf
from pandas import Series
from PyQt5.QtWidgets import (QWidget, QLabel, QSpinBox, QApplication, 
                             QTabWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                             QTextEdit, QGroupBox, QTextBrowser, QLineEdit, 
                             QProgressBar, QPushButton, QFileDialog)

import mago_min
import mago_max

"""
- Para restricciones de desigualdad, aplicar teoria de conjuntos e interceptar la zona que es valida
  para corregir y generar la poblacion, posiblemente creando un limite general que agrupe todas las 
  restricciones
- Para restricciones de igualdad....


"""

# Se reescribe la funcion ejemplo en el arhivo interno para evitar diversos problemas
fhand = open('function.py', 'w')
function_Exa = """
def f(x):
    return x[0] + x[1]
"""
fhand.write(function_Exa)
fhand.close()


class Gui_Mago(QWidget):
    def __init__(self):
        super().__init__()

        self.gui()

    def gui(self):
        """
        Interfaz grafica del mago
        """

        # Pestañas de opciones
        #     Pestaña de opciones generales

        #           Textos
        self.text_recursos = QLabel('Origen fobj')
        self.text_accion = QLabel('Accion')
        self.text_generaciones = QLabel('Generaciones')
        self.text_poblacion = QLabel('Poblacion')

        #           Widgets
        self.combobox_recurso = QComboBox()
        self.combobox_accion = QComboBox()
        self.spin_generaciones = QSpinBox()
        self.spin_poblacion = QSpinBox()

        self.combobox_accion.addItems(['Maximizar', 'Minimizar'])
        self.combobox_recurso.addItems(['Programa', 'Archivo'])
        self.spin_generaciones.setValue(50)
        self.spin_poblacion.setValue(50)
        self.spin_generaciones.setRange(1, 99999)
        self.spin_poblacion.setRange(1, 99999)

        #           Distribucion de espacios
        r1 = QHBoxLayout()
        r1.addWidget(self.text_recursos)
        r1.addStretch()
        r1.addWidget(self.combobox_recurso)

        r2 = QHBoxLayout()
        r2.addWidget(self.text_accion)
        r2.addStretch()
        r2.addWidget(self.combobox_accion)

        r4 = QHBoxLayout()
        r4.addWidget(self.text_generaciones)
        r4.addStretch()
        r4.addWidget(self.spin_generaciones)

        r5 = QHBoxLayout()
        r5.addWidget(self.text_poblacion)
        r5.addStretch()
        r5.addWidget(self.spin_poblacion)

        v1 = QVBoxLayout()        # Layout con todas las opciones generales
        v1.addLayout(r1)
        v1.addStretch()
        v1.addLayout(r2)
        v1.addStretch()
        v1.addLayout(r4)
        v1.addStretch()
        v1.addLayout(r5)

        opgen = QWidget()          
        opgen.setLayout(v1)

        opgraf = QWidget()


        #           Widget de pestañas
        self.tab_1 = QTabWidget()
        self.tab_1.addTab(opgen, 'Opciones generales')
        self.tab_1.addTab(opgraf, 'Opciones de graficas')

        # Cuadros de ingreso de funciones, restricciones y muestra de resultados

        self.text_ub = QLabel("Limites superiores")
        self.line_edit_ub = QLineEdit('10, 10')

        self.text_lb = QLabel("Limites inferiores")
        self.line_edit_lb = QLineEdit('-10, -10')

        v3 = QVBoxLayout()
        v3.addStretch()
        v3.addWidget(self.text_ub)
        v3.addWidget(self.line_edit_ub)
        v3.addStretch()
        v3.addWidget(self.text_lb)
        v3.addWidget(self.line_edit_lb)
        v3.addStretch()

        limites = QWidget()
        limites.setLayout(v3)

        restricciones = QWidget()

        #           Texto 'resultados' que acompaña el recuadro donde se ingresa la funcion objetivo
        self.text_fobj = QLabel('Funcion objetivo:')

        #           Cuadro donde se ingresa la funcion objetivo
        self.edittext_fobj = QTextEdit(function_Exa)

        #           widget de limites superiores e inferiores y restricciones
        self.tab_2 = QTabWidget()
        self.tab_2.addTab(limites, 'ub y lb')
        self.tab_2.addTab(restricciones, 'Restricciones')

        #           Texto 'resultados' que acompaña la salida de datos
        self.text_resultados = QLabel('Resultados:')

        #           Cuadro de salida de datos
        self.out_text = QTextBrowser()

        #           Boton de correr y barra de progreso
        
        self.bar = QProgressBar()
        self.correr = QPushButton('Correr')
        h1 = QHBoxLayout()
        h1.addStretch()
        h1.addWidget(self.bar)
        h1.addStretch()
        h1.addWidget(self.correr)
        h1.addStretch()


        # Ordenamiento de todas las secciones 
        #                   Columna vertical izquierda                
        vbox_2 = QVBoxLayout()
        vbox_2.addWidget(self.text_fobj)
        vbox_2.addWidget(self.edittext_fobj)
        vbox_2.addStretch()
        vbox_2.addWidget(self.tab_2)
        vbox_2.addStretch()

        gb_1 = QGroupBox('Ingreso de funcion y limites')
        gb_1.setLayout(vbox_2)

        
        vbox_1 = QVBoxLayout()
        vbox_1.addStretch()
        vbox_1.addWidget(self.tab_1)
        vbox_1.addStretch(1)
        vbox_1.addWidget(self.text_resultados)
        vbox_1.addWidget(self.out_text)
        vbox_1.addStretch(1)
        vbox_1.addLayout(h1)
        vbox_1.addStretch(1) 

        hbox_1 = QHBoxLayout()
        hbox_1.addLayout(vbox_1)
        hbox_1.addWidget(gb_1)


        self.setLayout(hbox_1)

        self.correr.clicked.connect(self.correr_mago)

        # Opciones iniciales
        self.bar.setHidden(True)
        self.texto_for_out = ""
        self.importado = False               # Indica si una fobj ya fue importada
        self.resize(650, 470)

        self.show()

    def correr_mago(self):

        try:

            # Se asigna la fobjetivo del origen requerido a una variable
            fObjetivo = self.find_function()

            # Se asignan los limites inferiores y superiores
            limite_inferior = (self.line_edit_lb.text()).split(',')
            limite_inferior = [float(k) for k in limite_inferior]

            limite_superior = (self.line_edit_ub.text()).split(',')
            limite_superior = [float(k) for k in limite_superior]


            for li, lu in zip(limite_inferior, limite_superior):
                if li >= lu:
                    raise TypeError("Interseccion de limites vacia")

        except AttributeError:
            # Error para funcion invalida
            self.print('Funcion objetivo no valida\nPor favor revise los parametros de entrada\n')          

        except ValueError:
            # Error para limites invalidos
            self.print('Limites no validos\nPor favor revise los parametros de entrada\n')       

        except IndexError:
            # Error para limites invalidos en la funcion
            self.print('Limites no acordes a la funcion a optimizar\nPor favor revise los parametros de entrada\n')

        except ZeroDivisionError:
            # Error para division por 0
            self.print('Uno de los limites produce una division por 0, corregir\n')

        except TypeError:
            # Errir para interseccion de los limites 0 o vacia
            self.print("Limites inferiores mayores o iguales a los superiores en una o mas componentes\nPor favor revise los parametros de entrada\n")

        else:

            # Se asigna el numero de generaciones y poblacion a variables
            n_gen = self.spin_generaciones.value()
            n_ind = self.spin_poblacion.value()   

            # Se muestra la barra de progreso
            self.bar.setHidden(False)

            # Se indica en el recuadro de salida de datos que se ejecuta el mago 
            self.print("Corriendo\n")

            # Lanzamiento de algoritmo mago, maximizacion o minimizacion
            try:
                if self.combobox_accion.currentText() == "Maximizar":
                    self.resultados = self.run_mago_max(limite_inferior, 
                                                        limite_superior, 
                                                        n_ind, n_gen, fObjetivo)

                else:
                    self.resultados = self.run_mago_min(limite_inferior, 
                                                        limite_superior, 
                                                        n_ind, n_gen, fObjetivo)
            except:
                self.print("""A ocurrido un error al ejecutar Mago, por favor revise los parametros
                    Pudo haber ocurrido un error tipo algebraico como division por 0""")


            # Se muestran los resultados obtenidos al usuario en el recuadro de salida de datos
            self.print(self.resultados[0] + '\n')

            # Se oculta la barra de progreso
            self.bar.setHidden(True)

    def find_function(self):
        """
        Se recolecta la funcion objetivo del recurso elegido
        El recuadro de texto o un archivo.py de eleccion
        """

        # Eleccion de archivo o recuadro para fobj
        if self.combobox_recurso.currentText() == "Programa":

            # Guarda en un archivo interno del programa la funcion del recuadro
            fhand = open('function.py', 'w')
            fhand.write(self.edittext_fobj.toPlainText())
            fhand.close()

            # Se muestra en el recuadro de salida la funcion a optimizar
            self.print('------------------\n')

            # Se importa, obtiene y asigna a una variable la fobjetivo del recuadro
            # En caso de que se corra por segunda vez, elimina la fobj y la reimporta
            if self.importado:
                del modules['function']

            import function
            fObjetivo = function.f

            self.importado = True


        else:
            # Pide la ruta del programa 
            filename = QFileDialog.getOpenFileName(self, 'Open File', getenv('HOME'))

            # fhand es el archivo con la funcion externa
            fhand = open(filename[0], 'r')
            texto = fhand.read()

            # Se obtiene el nombre de la funcion en el arhivo de texto
            fobj_archivo = findall('def (.+)\(', texto)[0]

            # Se reemplaza el nombre de la funcion por f(x) para una correcto manejo
            texto = sub('def .+\(', 'def f(', texto)


            # fhand2 es el arhivo interno donde se guardara la funcion a optimizar
            fhand2 = open('function.py', 'w')
            fhand2.write('\n' + texto + '\n')
            fhand2.close()   

            # Se muestra en el recuadro de salida la funcion a optimizar
            self.print('------------------\n' + 'Optimizando: ' + fobj_archivo + '\n')

            # Se importa, obtiene y asigna a una variable la fobjetivo externa
            # En caso de que se corra por segunda vez, elimina la fobj y la reimporta
            if self.importado:
                del modules['function']

            import function
            fObjetivo = function.f

            self.importado = True


        return fObjetivo

    def print(self, texto):
        """
        Funcion que recibe un str
        Muestra el texto anterior mas el nuevo str en el recuadro de salida de texto,
        tambien ubica el scrollbar en la parte inferior
        """
        self.texto_for_out = self.texto_for_out + texto
        self.out_text.setText(self.texto_for_out)
        self.out_text.verticalScrollBar().setValue(self.out_text.verticalScrollBar().maximum())            

    def run_mago_max(self, lmt_inferior, lmt_superior, n, ng, fObjetivo):


        # Generacion de la poblacion inicial
        poblacion = mago_max.generarPoblacion(lmt_inferior, lmt_superior, n)


        # Serie donde se guarda el mejor valor de fobj de cada generacion, para fines ilustrativos
        best_fobj = Series()


        # Lista donde se guardan todos los datos que seran regresados por la funcion
        datos = list()


        for i in range(ng):


            self.bar.setValue((100 / n) * (i + 1))


            # print('Generacion numero: ', i + 1)

            # Evaluar poblacion en fobj
            resultados = mago_max.evaluarPoblacion(poblacion, fObjetivo)


            # Se agrega el mejor individuo de la generacion a best_fobj
            best_fobj = best_fobj.append(Series({i + 1: resultados.index[-1]}))


            # Calculos estadisticos varios
            s = cov(poblacion, rowvar=False)
            sd = sqrt(diag(s))   
            media = mean(poblacion, axis=0)           
                    
            mini = subtract(media, multiply(0.5, sd))
            maxi = add(media, multiply(0.5, sd))
        
            mini1 = subtract(media, sd)
            maxi1 = add(media, sd)


            # Calculo de las cardinalidades
            poblacionRegion_1 = mago_max.filtrarIndividuosRegion(poblacion, mini, maxi)
            poblacionRegion_2 = mago_max.filtrarIndividuosRegion(poblacion, mini1, maxi1)


            n1 = sum(poblacionRegion_1)           
            if n1 < 0:
                n1 = 0

            n2 = sum(poblacionRegion_2) - n1 - 1
            if n2 < 0:
                n2 = 0

            n3 = n - n1 - n2

            sn = multiply(s, 1 / linalg.norm(s, inf))


            # Si hay individuos en n1, calcular diferencias y hacerlos competir
            if n1 > 0:
                resultados = mago_max.competenciaG1(resultados, n1, sn, fObjetivo, lmt_inferior, lmt_superior)
                grupo_mejores = resultados.iloc[-n1:] 


            # Poblacion de la siguiente generacion
            poblacion = list()

            if n1 != 0:
                poblacion.extend(grupo_mejores)
            else:
                # En caso de que n1 sea 0, guarda el mejor individuo para la proxima generacion
                # y resta 1 a n3 o n2 para mantener la poblacion en n individuos
                poblacion.append(resultados.iat[-1])
                if n3 != 0:
                    n3 -= 1
                else:
                    n2 -= 1

            if n2 != 0:
                poblacion.extend(mago_max.generarPoblacion(mini, maxi, n2))

            if n3 != 0:
                poblacion.extend(mago_max.generarPoblacion(lmt_inferior, lmt_superior, n3)) 

        valores_optimos = [round(n, 4) for n in resultados.iat[-1]]
        fobj_optima = round(resultados.index[-1], 4)

        datos.append("\nResultado:\n{} \n\nFuncion objetivo:\n{}\n ".format(valores_optimos, fobj_optima))
        datos.append(best_fobj)

        return datos

    def run_mago_min(self, lmt_inferior, lmt_superior, n, ng, fObjetivo):

        # Generacion de la poblacion inicial
        poblacion = mago_min.generarPoblacion(lmt_inferior, lmt_superior, n)


        # Serie donde se guarda el mejor valor de fobj de cada generacion, para fines ilustrativos
        best_fobj = Series()


        # Lista donde se guardan todos los datos que seran regresados por la funcion
        datos = list()


        for i in range(ng):

            self.bar.setValue((100 / n) * (i + 1))

            #  print('Generacion numero: ', i + 1)

            # Evaluar poblacion en fobj
            resultados = mago_min.evaluarPoblacion(poblacion, fObjetivo)


            # Se agrega el mejor individuo de la generacion a best_fobj
            best_fobj = best_fobj.append(Series({i + 1: resultados.index[0]}))


            # Calculos estadisticos varios
            s = cov(poblacion, rowvar=False)
            sd = sqrt(diag(s))   
            media = mean(poblacion, axis=0)           
                    
            mini = subtract(media, multiply(0.5, sd))
            maxi = add(media, multiply(0.5, sd))

            mini1 = subtract(media, sd)
            maxi1 = add(media, sd)


            # Calculo de las cardinalidades
            poblacionRegion_1 = mago_min.filtrarIndividuosRegion(poblacion, mini, maxi)
            poblacionRegion_2 = mago_min.filtrarIndividuosRegion(poblacion, mini1, maxi1)


            n1 = sum(poblacionRegion_1)           
            if n1 < 0:
                n1 = 0

            n2 = sum(poblacionRegion_2) - n1 - 1
            if n2 < 0:
                n2 = 0

            n3 = n - n1 - n2

            sn = multiply(s, 1 / linalg.norm(s, inf))


            # Si hay individuos en n1, calcular diferencias y hacerlos competir
            if n1 > 0:
                resultados = mago_min.competenciaG1(resultados, n1, sn, fObjetivo, lmt_inferior, lmt_superior)
                grupo_mejores = resultados.iloc[:n1] 
    

            # Poblacion de la siguiente generacion
            poblacion = list()
    
            if n1 != 0:
                poblacion.extend(grupo_mejores) 
            else:
                # En caso de que n1 sea 0, guarda el mejor individuo para la proxima generacion
                # y resta 1 a n3 o n2 para mantener la poblacion en n individuos
                poblacion.append(resultados.iat[0])
                if n3 != 0:
                    n3 -= 1
                else:
                    n2 -= 1

            if n2 != 0:
                poblacion.extend(mago_min.generarPoblacion(mini, maxi, n2))

            if n3 != 0:
                poblacion.extend(mago_min.generarPoblacion(lmt_inferior, lmt_superior, n3))


        datos.append("\nResultado:\n{} \n\nFuncion objetivo:\n{}\n ".format(resultados.iat[0], resultados.index[0]))
        datos.append(best_fobj)


        return datos


app = QApplication(argv)
a_window = Gui_Mago()
exit(app.exec_())
