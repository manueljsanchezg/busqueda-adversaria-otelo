from tqdm import tqdm # Librería para barras de progreso
import pandas as pd
import otelo
import mcts

partidas = 30
ganadas_negras = 0
ganadas_blancas = 0

df_estados_partidas = pd.DataFrame()

def crear_fila(tablero, turno, ganador):
    fila = tablero.copy()
    fila["turno"] = turno
    fila["ganador"] = ganador
    return fila

for i in tqdm(range(partidas)):

    turno = 1

    tablero = otelo.crear_tablero()

    #otelo.mostrar_tablero(tablero)

    partida_actual = []

    while True:

        if not otelo.jugador_puede_mover(tablero, 1) and not otelo.jugador_puede_mover(tablero, 2):
            ganador, blancas, negras = otelo.ganador(tablero)
            if ganador == 1:
                ganadas_negras += 1
                print("Las negras ganan la partida")
            elif ganador == 2:
                ganadas_blancas += 1
                print("Las blancas ganan la partida")
            print("Las negras han conseguido: ", negras)
            print("Las blancas han conseguido: ", blancas)
            for fila in partida_actual:
                df_estados_partidas = pd.concat([df_estados_partidas, pd.DataFrame([fila])], ignore_index=True)
            break


        if not otelo.jugador_puede_mover(tablero, turno):
            turno = 3 - turno
            continue

        if turno == 1:
            movimiento = mcts.mcts_uct(tablero, turno, iteraciones=500)
        elif turno == 2:
            movimiento = mcts.mcts_uct(tablero, turno, iteraciones=500, red_neuronal=False)

        otelo.poner_ficha(tablero, movimiento[0], movimiento[1], turno)

        ganador, blancas, negras = otelo.ganador(tablero)

        nueva_fila = crear_fila(tablero, turno, ganador)
        partida_actual.append(nueva_fila)
        
        turno = 3 - turno

#df_estados_partidas.to_csv("partidas_ia_vs_ia.csv", index=False)
print("Partidas ganadas por las negras: ", ganadas_negras)
print("Partidas ganadas por las blancas: ", ganadas_blancas)