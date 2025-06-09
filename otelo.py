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
    simbolos = {0: '.', 1: 'N', 2: 'B'}
    print("  " + " ".join(str(j) for j in range(0, 8)))
    for i in range(0, 8):
        fila = [simbolos[tablero[(i, j)]] for j in range(0, 8)]
        print(f"{i} " + " ".join(fila))
        
def poner_ficha(tablero, fila, columna, turno):
    valido, fichas_a_voltear = es_movimiento_valido(tablero, fila, columna, turno)
    if valido:
        tablero[(fila, columna)] = turno
        for x,y in fichas_a_voltear:
            tablero[(x,y)] = turno
    else:
        return 'Movimiento inválido'    
    

def es_movimiento_valido(tablero, fila, columna, turno):
    fichas_a_voltear = []
    
    if tablero[(fila, columna)] != 0:
        return False, []
    
    enemigo = 3 - turno
    direcciones = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in direcciones:
        temp = []
        x= fila + dx
        y = columna + dy
        hay_enemigo = False

        while 0 <= x < 8 and 0 <= y < 8 and tablero[(x, y)] == enemigo:
            temp.append((x,y))
            x += dx
            y += dy
            hay_enemigo = True
        if hay_enemigo and 0 <= x < 8 and 0 <= y < 8 and tablero[(x, y)] == turno:
            fichas_a_voltear.extend(temp)
        
    if len(fichas_a_voltear) > 0:
        return True, fichas_a_voltear

    return False, []

def posibles_movimientos(tablero, turno):
    posibles_movimientos = dict()
    for i in range(8):
        for j in range(8):
            if tablero[(i, j)] == 0:
                valido, fichas_volteadas = es_movimiento_valido(tablero, i, j, turno)
                if valido:
                    posibles_movimientos[(i,j)] = len(fichas_volteadas)
    return posibles_movimientos

def jugador_puede_mover(tablero, turno):
    for i in range(8):
        for j in range(8):
            if tablero[(i, j)] == 0 and es_movimiento_valido(tablero, i, j, turno)[0]:
                return True
    return False

def ganador(tablero):
    blancas = 0
    negras = 0
    ganador = 0
    for i in range(0,8):
        for j in range(0, 8):
            if tablero[(i,j)] == 1:
                negras += 1
            elif tablero[(i,j)] == 2:
                blancas += 1
    if blancas > negras:
        ganador = 2
    elif negras > blancas:
        ganador = 1
    else:
        ganador = 0

    return ganador, blancas, negras
