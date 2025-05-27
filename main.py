EMPTY = 0
BLACK = 1
WHITE = 2

TURN = 2

DRAW = 0
ACTIVE_WIN = 1
ACTIVE_LOSE = -1

#(3,3) -> negra
#(3,4) -> blanca
#(4,3) -> blanca
#(4,4) -> negra

def crear_tablero():
    res = dict()
    for i in range(0, 8):
        for j in range(0, 8):
            res[(i,j)] = 0

    res[(3, 3)] = 1
    res[(4, 4)] = 1
    res[(3, 4)] = 2
    res[(4, 3)] = 2

    return res

def mostrar_tablero(tablero):
    simbolos = {0: '.', 1: 'B', 2: 'W'}

    print("  " + " ".join(str(j) for j in range(0, 8)))
    for i in range(0, 8):
        fila = [simbolos[tablero[(i, j)]] for j in range(0, 8)]
        print(f"{i} " + " ".join(fila))
        
def poner_ficha(tablero, fila, columna, turno):
    if es_movimiento_valido(tablero, fila, columna, turno):
        tablero[fila, columna] = turno
        return mostrar_tablero(tablero)
    else:
        return 'Movimiento inválido'    
    

def es_movimiento_valido(tablero, fila, columna, turno):
    if tablero[(fila, columna)] != 0:
        return False

    enemigo = 3 - turno
    direcciones = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in direcciones:
        x, y = fila + dx, columna + dy
        hay_enemigo = False

        while 0 <= x < 8 and 0 <= y < 8 and tablero[(x, y)] == enemigo:
            x += dx
            y += dy
            hay_enemigo = True

        if hay_enemigo and 0 <= x < 8 and 0 <= y < 8 and tablero[(x, y)] == turno:
            return True

    return False
                

def jugador_puede_mover(tablero, turno):
    for i in range(8):
        for j in range(8):
            if tablero[(i, j)] == EMPTY and es_movimiento_valido(tablero, i, j, turno):
                return True
    return False
            


tablero = crear_tablero()
turno = 2

while True:
    mostrar_tablero(tablero)

    if not jugador_puede_mover(tablero, turno):
        turno = 3 - turno
        continue

    if turno == 2:
        print("Negras, indique su movimiento")
    else:
        print("Blancas, indique su movimiento")

    coordenas = input("Formato fila,columna (ej: 2,3): ")

    fila = int(coordenas.split(",")[0])
    columna = int(coordenas.split(",")[1])

    resultado = poner_ficha(tablero, fila, columna, turno)

    if resultado == 'Movimiento inválido':
        print(resultado)
        continue

    turno = 3 - turno

