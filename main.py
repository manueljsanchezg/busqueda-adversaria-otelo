import otelo
import mcts

tablero = otelo.crear_tablero()

turno = 1

otelo.mostrar_tablero(tablero)

while True:

    if not otelo.jugador_puede_mover(tablero, 1) and not otelo.jugador_puede_mover(tablero, 2):
        ganador, blancas, negras = otelo.ganador(tablero)
        if ganador == 1:
            print("Las negras ganan la partida")
        elif ganador == 2:
            print("Las blancas ganan la partida")
        print("Las negras han conseguido: ", negras)
        print("Las blancas han conseguido: ", blancas)
        break


    if not otelo.jugador_puede_mover(tablero, turno):
        turno = 3 - turno
        continue

    if turno == 2:
        
        movimiento = mcts.mcts_uct(tablero, turno, iteraciones=1000)
        print(movimiento)

        otelo.poner_ficha(tablero, movimiento[0], movimiento[1], turno)

        otelo.mostrar_tablero(tablero)
        
        turno = 3 - turno

    else:
        print("Negras, indique su movimiento")

        try: 

            print("Posibles movimientos: ", otelo.posibles_movimientos(tablero, turno))

            coordenas = input("Formato fila,columna (ej: 2,3): ")
        
            fila = int(coordenas.split(",")[0])
        
            columna = int(coordenas.split(",")[1])

            resultado = otelo.poner_ficha(tablero, fila, columna, turno)

            otelo.mostrar_tablero(tablero)

            if resultado == 'Movimiento inválido':
                print(resultado)
                continue

            turno = 3 - turno

        except ValueError:
            print("Debes ingresar 2 números separados por coma")
        except KeyError:
            print("Debes ingresar 2 números válidos enter 0 y 7")
        except IndexError:
            print("Debes ingresar 2 números válidos enter 0 y 7")


    

    
