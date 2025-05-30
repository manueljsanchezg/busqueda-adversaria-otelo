import random
import math
import otelo

class Nodo:
    def __init__(self, tablero, turno, padre=None, accion = None):
        self.estado = tablero
        self.turno = turno
        self.padre = padre
        self.hijos = []
        self.acciones_posibles = otelo.posibles_movimientos(tablero, turno)
        self.acciones_hechas = []
        self.accion = accion
        self.r_acum = 0
        self.n_visitas = 0


def mcts_uct(tablero, turno, iteraciones=100, ia_vs_ia = False):
    raiz = Nodo(tablero, turno)
    for i in range(0, iteraciones):
        nuevo_nodo = seleccion(raiz)
        res_simulacion = simula(nuevo_nodo.estado, nuevo_nodo.turno, ia_vs_ia)
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
            nodo.hijos.append(nuevo_nodo)
            return nuevo_nodo


def mejor_sucesor_uct(nodo):
    c_p = 0.7
    n_s0 = nodo.n_visitas
    uct_hijos = []
    posicion = 0
    for hijo in nodo.hijos:
        if hijo.n_visitas == 0:
            uct = float('inf')
        else:
            q_s = hijo.r_acum
            n_s = hijo.n_visitas
            uct = (q_s/n_s) + 2*c_p*math.sqrt(math.log(n_s0)/n_s)
        
        uct_hijos.append((posicion, uct))

    if not uct_hijos or len(uct_hijos) == 0:
        return nodo

    mejor_hijo = max(uct_hijos, key=lambda x:x[1])

    return nodo.hijos[mejor_hijo[0]]

def simula(tablero, turno, ia_vs_ia):
    nuevo_tablero = tablero.copy()
    nuevo_turno = turno
    while True:
        if not otelo.jugador_puede_mover(nuevo_tablero, 1) and not otelo.jugador_puede_mover(nuevo_tablero, 2):
            ganador, blancas, negras = otelo.ganador(nuevo_tablero)
            
            if not ia_vs_ia:
                if blancas == negras:
                    return 0
                elif ganador == 2:
                    return 1
                elif ganador == 1:
                    return -1
            else:
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
        
