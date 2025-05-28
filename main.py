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
    valido, fichas_a_voltear = es_movimiento_valido(tablero, fila, columna, turno)
    if valido:
        tablero[fila, columna] = turno

        for x,y in fichas_a_voltear:
            tablero[x,y] = turno

        return mostrar_tablero(tablero)
    else:
        return 'Movimiento inválido'    
    

def es_movimiento_valido(tablero, fila, columna, turno):
    fichas_a_voltear = []
    camino = []
    
    if tablero[(fila, columna)] != 0:
        return False, []
    
    enemigo = 3 - turno
    direcciones = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in direcciones:
        x, y = fila + dx, columna + dy
        hay_enemigo = False

        while 0 <= x < 8 and 0 <= y < 8 and tablero[(x, y)] == enemigo:
            camino = [(x,y)]
            x += dx
            y += dy
            hay_enemigo = True
        if hay_enemigo and 0 <= x < 8 and 0 <= y < 8 and tablero[(x, y)] == turno:
            fichas_a_voltear.extend(camino)
            return True, fichas_a_voltear

    return False, []

def posibles_movimientos(tablero, turno):
    posibles_movimientos = dict()
    for i in range(8):
        for j in range(8):
            if tablero[(i, j)] == EMPTY and es_movimiento_valido(tablero, i, j, turno)[0]:
                posibles_movimientos[(i,j)] = len(es_movimiento_valido(tablero, i, j, turno)[1])
    return posibles_movimientos

def jugador_puede_mover(tablero, turno):
    for i in range(8):
        for j in range(8):
            if tablero[(i, j)] == EMPTY and es_movimiento_valido(tablero, i, j, turno)[0]:
                return True
    return False

def ganador(tablero):
    blancas = 0
    negras = 0
    ganador = ''
    for i in range(0,8):
        for j in range(0, 8):
            if tablero[(i,j)] == 1:
                negras += 1
            elif tablero[(i,j)] == 2:
                blancas += 1
    if blancas > negras:
        ganador = 'Ganan las blancas'
    elif negras > blancas:
        ganador = 'Ganan las negras'

    return ganador, blancas, negras


tablero = crear_tablero()

turno = 1

mostrar_tablero(tablero)

while True:

    if not jugador_puede_mover(tablero, 1) and not jugador_puede_mover(tablero, 2):
        ganador, blancas, negras = ganador(tablero)
        print(ganador)
        print("Las negras han conseguido: ", negras)
        print("Las blancas han conseguido: ", blancas)
        break


    if not jugador_puede_mover(tablero, turno):
        turno = 3 - turno
        continue

    if turno == 2:
        print("Blancas, indique su movimiento")
    else:
        print("Negras, indique su movimiento")


    try: 

        print("Posibles movimientos: ", posibles_movimientos(tablero, turno))

        coordenas = input("Formato fila,columna (ej: 2,3): ")
        
        fila = int(coordenas.split(",")[0])
        
        columna = int(coordenas.split(",")[1])

        resultado = poner_ficha(tablero, fila, columna, turno)

        if resultado == 'Movimiento inválido':
            print(resultado)
            continue

        turno = 3 - turno

    except ValueError:
        print("Debes ingresar 2 números separados por coma")

    
