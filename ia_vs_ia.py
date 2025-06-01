from tqdm import tqdm # Librería para barras de progreso
import otelo
import mcts

partidas = 10
ganadas_negras = 0
ganadas_blancas = 0

for i in tqdm(range(partidas)):

    # Alternancia de primer jugador

    turno = 1

    tablero = otelo.crear_tablero()

    #otelo.mostrar_tablero(tablero)

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
            break


        if not otelo.jugador_puede_mover(tablero, turno):
            turno = 3 - turno
            continue

        
        
        movimiento = mcts.mcts_uct(tablero, turno, iteraciones=500, ia_vs_ia=True)
        #print(movimiento)

        otelo.poner_ficha(tablero, movimiento[0], movimiento[1], turno)

        #otelo.mostrar_tablero(tablero)
        
        turno = 3 - turno

print("Partidas ganadas por las negras: ", ganadas_negras)
print("Partidas ganadas por las blancas: ", ganadas_blancas)