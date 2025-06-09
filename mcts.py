import random
import numpy as np
import math
import otelo
from keras.models import load_model

red_otelo = load_model("red_otelo.h5")

class Nodo:
    def __init__(self, tablero, turno, padre=None, accion = None):
        self.estado = tablero
        self.turno = turno
        self.padre = padre
        self.hijos = []
        acciones = list(otelo.posibles_movimientos(tablero, turno).items())
        random.shuffle(acciones)
        self.acciones_posibles = dict(acciones)        
        self.acciones_hechas = []
        self.accion = accion
        self.r_acum = 0
        self.n_visitas = 0


def mcts_uct(tablero, turno, iteraciones=100, red_neuronal = False):
    raiz = Nodo(tablero, turno)
    for i in range(0, iteraciones):
        nuevo_nodo = seleccion(raiz)
        if red_neuronal == True:
            res_simulacion = simula_red(nuevo_nodo.estado, nuevo_nodo.turno)
        elif red_neuronal == False:
            res_simulacion = simula(nuevo_nodo.estado, nuevo_nodo.turno)
        retropropaga(nuevo_nodo, res_simulacion)

    return mejor_sucesor_uct(raiz).accion

def seleccion(nodo):
    if not otelo.jugador_puede_mover(nodo.estado, 1) and not otelo.jugador_puede_mover(nodo.estado, 2):
        return nodo
    
    if len(nodo.acciones_hechas) != len(nodo.acciones_posibles):
        return expande(nodo)
    
    mejor_hijo = mejor_sucesor_uct(nodo)
    
    if mejor_hijo is None or mejor_hijo == nodo:
        return nodo

    return seleccion(mejor_hijo)
    

def expande(nodo):
    for accion,_ in nodo.acciones_posibles.items():
        if accion not in nodo.acciones_hechas:
            nuevo_tablero = nodo.estado.copy()
            otelo.poner_ficha(nuevo_tablero, accion[0], accion[1], nodo.turno)
            nodo.acciones_hechas.append(accion)
            nuevo_nodo = Nodo(nuevo_tablero, padre= nodo, turno= 3-nodo.turno, accion=accion)
            nuevo_nodo.n_visitas += 1
            nodo.hijos.append(nuevo_nodo)
            return nuevo_nodo


def mejor_sucesor_uct(nodo):
    c_p = 1.4142
    n_s0 = nodo.n_visitas
    uct_hijos = []
    posicion = 0
    for hijo in nodo.hijos:
        q_s = hijo.r_acum
        n_s = hijo.n_visitas
        uct = (q_s/n_s) + 2*c_p*math.sqrt(math.log(n_s0)/n_s)
        
        uct_hijos.append((posicion, uct))

    if not uct_hijos or len(uct_hijos) == 0:
        return nodo

    mejor_hijo = max(uct_hijos, key=lambda x:x[1])

    return nodo.hijos[mejor_hijo[0]]

def simula(tablero, turno):
    nuevo_tablero = tablero.copy()
    nuevo_turno = turno
    while True:
        if not otelo.jugador_puede_mover(nuevo_tablero, 1) and not otelo.jugador_puede_mover(nuevo_tablero, 2):
            ganador, blancas, negras = otelo.ganador(nuevo_tablero)
            
            if blancas == negras:
                return 0
            elif ganador == turno:
                return 1
            elif ganador != turno:
                return -1    
        
        if not otelo.jugador_puede_mover(nuevo_tablero, nuevo_turno):
            nuevo_turno = 3 - nuevo_turno
            continue

        movimiento = random.choice(list(otelo.posibles_movimientos(nuevo_tablero, nuevo_turno)))

        #movimientos = otelo.posibles_movimientos(nuevo_tablero, nuevo_turno)
        #movimiento = maximiza_fichas_volteadas(movimientos)

        otelo.poner_ficha(nuevo_tablero, movimiento[0], movimiento[1], nuevo_turno)

        nuevo_turno = 3 - nuevo_turno

def maximiza_fichas_volteadas(movimientos):
    return max(movimientos.items(), key=lambda x: x[1])[0]

def retropropaga(nodo, res_simulacion):
    while nodo is not None:
        nodo.r_acum += res_simulacion
        nodo.n_visitas += 1
        res_simulacion *= -1 
        nodo = nodo.padre
        

def representar_tablero_para_red(tablero, turno):
    entrada = []
    for i in range(8):
        for j in range(8):
            entrada.append(float(tablero[(i, j)]))
    entrada.append(float(turno))
    return entrada

def simula_red(tablero, turno):
    entrada = representar_tablero_para_red(tablero, turno)
    prediccion = red_otelo.predict(np.array([entrada]), verbose=0)[0][0]
    return prediccion