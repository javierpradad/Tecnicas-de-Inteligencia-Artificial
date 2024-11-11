from defines import *
import time

# Point (x, y) if in the valid position of the board.
def isValidPos(x,y):
    return x>0 and x<Defines.GRID_NUM-1 and y>0 and y<Defines.GRID_NUM-1
    
def init_board(board):
    for i in range(21):
        board[i][0] = board[0][i] = board[i][Defines.GRID_NUM - 1] = board[Defines.GRID_NUM - 1][i] = Defines.BORDER
    for i in range(1, Defines.GRID_NUM - 1):
        for j in range(1, Defines.GRID_NUM - 1):
            board[i][j] = Defines.NOSTONE
            
def make_move(board, move, color):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color

def unmake_move(board, move):
    board[move.positions[0].x][move.positions[0].y] = Defines.NOSTONE
    board[move.positions[1].x][move.positions[1].y] = Defines.NOSTONE

def is_win_by_premove(board, preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for direction in directions:
        for i in range(len(preMove.positions)):
            count = 0
            position = preMove.positions[i]
            n = x = position.x
            m = y = position.y
            movStone = board[n][m]
            
            if (movStone == Defines.BORDER or movStone == Defines.NOSTONE):
                return False
                
            while board[x][y] == movStone:
                x += direction[0]
                y += direction[1]
                count += 1
            x = n - direction[0]
            y = m - direction[1]
            while board[x][y] == movStone:
                x -= direction[0]
                y -= direction[1]
                count += 1
            if count >= 6:
                return True
    return False

def get_msg(max_len):
    buf = input().strip()
    return buf[:max_len]

def log_to_file(msg):
    g_log_file_name = Defines.LOG_FILE
    try:
        with open(g_log_file_name, "a") as file:
            tm = time.time()
            ptr = time.ctime(tm)
            ptr = ptr[:-1]
            file.write(f"[{ptr}] - {msg}\n")
        return 0
    except Exception as e:
        print(f"Error: Can't open log file - {g_log_file_name}")
        return -1

def move2msg(move):
    if move.positions[0].x == move.positions[1].x and move.positions[0].y == move.positions[1].y:
        msg = f"{chr(ord('S') - move.positions[0].x + 1)}{chr(move.positions[0].y + ord('A') - 1)}"
        return msg
    else:
        msg = f"{chr(move.positions[0].y + ord('A') - 1)}{chr(ord('S') - move.positions[0].x + 1)}" \
              f"{chr(move.positions[1].y + ord('A') - 1)}{chr(ord('S') - move.positions[1].x + 1)}"
        return msg

def msg2move(msg):
    move = StoneMove()
    if len(msg) == 2:
        move.positions[0].x = move.positions[1].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = move.positions[1].y = ord(msg[0]) - ord('A') + 1
        move.score = 0
        return move
    else:
        move.positions[0].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = ord(msg[0]) - ord('A') + 1
        move.positions[1].x = ord('S') - ord(msg[3]) + 1
        move.positions[1].y = ord(msg[2]) - ord('A') + 1
        move.score = 0
        return move

def print_board(board, preMove=None):
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{chr(ord('A') - 1 + i)}", end=" ")
        for j in range(1, Defines.GRID_NUM - 1):
            x = Defines.GRID_NUM - 1 - j
            y = i
            stone = board[x][y]
            if stone == Defines.NOSTONE:
                print(" -", end="")
            elif stone == Defines.BLACK:
                print(" O", end="")
            elif stone == Defines.WHITE:
                print(" *", end="")
        print(" ", end="")        
        print(f"{chr(ord('A') - 1 + i)}", end="\n")
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))

def print_score(move_list, n):
    board = [[0] * Defines.GRID_NUM for _ in range(Defines.GRID_NUM)]
    for move in move_list:
        board[move.x][move.y] = move.score

    print("  " + "".join([f"{i:4}" for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{i:2}", end="")
        for j in range(1, Defines.GRID_NUM - 1):
            score = board[i][j]
            if score == 0:
                print("   -", end="")
            else:
                print(f"{score:4}", end="")
        print()

def ver_victoria(board):
    direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]
    # Iteramos sobre todo el tablero
    for fila in range(1, Defines.GRID_NUM - 1):
        for col in range(1, Defines.GRID_NUM - 1):

            color_actual = board[fila][col]
            #print(f"FILA: {fila}, COLUMNA: {col}, color actual:{color_actual}")

            # Verificar si la celda actual pertenece al color que estamos revisando
            if board[fila][col] == Defines.NOSTONE:
                continue

            #print_board(board)
            for dx, dy in direcciones:
                count = 1
                longitud = contar_cadena(board, fila, col, dx, dy, color_actual) 
                count += longitud
                #print(f"segundo count: {count}")
                longitud = contar_cadena(board, fila, col, -dx, -dy, color_actual) 
                count += longitud
                #print(f"tercer count: {count}")
                #print("-----------------------------------------------------------------------")
                if count >= 6:
                    return True
            
    return False

def ver_empate(board):
    if board == None:
        return False

    for fila in board:
        if Defines.NOSTONE in fila:
            return False
    return True

"""def contar_piedras(color, board, jugador):
    piedras = 0
    direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for fila in range(1, Defines.GRID_NUM - 1):
        for col in range(1, Defines.GRID_NUM - 1):
            if board[fila][col] == color:
                for dx, dy in direcciones:
                    longitud_cadena, es_cadena_viva = contar_cadena(board, fila, col, dx, dy, color)
                    if es_cadena_viva:
                        piedras += 2 ** (longitud_cadena - 1)
                    if longitud_cadena >= 4 and color == jugador and es_cadena_viva:
                        piedras += 200

    return piedras
    """


"""def contar_cadena(board, fila, col, dx, dy, color):
    consecutivas_adelante = 0
    consecutivas_atras = 0
    n = len(board)

    for i in range(1, 6):
        nueva_fila = fila + i * dx
        nueva_col = col + i * dy

        if nueva_fila < 0 or nueva_fila >= n or nueva_col < 0 or nueva_col >= n:
            break

        #print(f"fila: {nueva_fila}     columna: {nueva_col}")
        if board[nueva_fila][nueva_col] == color:
            consecutivas_adelante += 1
        else:
            break

    for i in range(1, 6):
        nueva_fila = fila - i * dx
        nueva_col = col - i * dy

        if nueva_fila < 0 or nueva_fila >= n or nueva_col < 0 or nueva_col >= n:
            break

        if board[nueva_fila][nueva_col] == color:
            consecutivas_atras += 1
        else:
            break
        if consecutivas_atras >=4:
            print(fila, col)


    consecutivas = consecutivas_atras + consecutivas_adelante
    if consecutivas > 3:
        print("-----------")
        print(consecutivas_adelante)
        print(consecutivas_atras)
        print(consecutivas)
        print("-----------")
    es_cadena_viva = False

    # Chequear extremo positivo
    extremo_positivo_libre = False
    nueva_fila = fila + consecutivas * dx
    nueva_col = col + consecutivas * dy
    if 0 <= nueva_fila < n and 0 <= nueva_col < n and board[nueva_fila][nueva_col] == Defines.NOSTONE:
        extremo_positivo_libre = True

    # Chequear extremo negativo
    extremo_negativo_libre = False
    nueva_fila = fila - consecutivas * dx
    nueva_col = col - consecutivas * dy
    if 0 <= nueva_fila < n and 0 <= nueva_col < n and board[nueva_fila][nueva_col] == Defines.NOSTONE:
        extremo_negativo_libre = True

    # La cadena es "viva" si tiene al menos un extremo libre
    es_cadena_viva = extremo_positivo_libre or extremo_negativo_libre

    return consecutivas, es_cadena_viva"""

def contar_piedras(color, board, jugador, movimientos_ia, movimientos_jugador):
    piedras = 0
    direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]

    movimientos = movimientos_jugador if color == jugador  else movimientos_ia

    for move in movimientos:
        last_move = move.positions[1]
        if board[last_move.x][last_move.y] == color:
            for dx, dy in direcciones:
                longitud_cadena = contar_cadena(board, last_move.x, last_move.y, dx, dy, color)
                piedras += 2 ** (longitud_cadena - 1)
    return piedras
    

def contar_cadena(board, fila, col, dx, dy, color):
    consecutivas = 0
    n = len(board)

    for i in range(1, 6):
        nueva_fila = fila + i * dx
        nueva_col = col + i * dy

        if nueva_fila < 0 or nueva_fila >= n or nueva_col < 0 or nueva_col >= n:
            break

        #print(f"fila: {nueva_fila}     columna: {nueva_col}")
        if board[nueva_fila][nueva_col] == color:
            consecutivas += 1
        else:
            break

    #print(f"piedras consecutivas: {consecutivas}")
    return consecutivas

def calcular_posicion_fichas(board, color_ia, color_jugador, movimientos_ia, movimientos_jugador):
    puntuacion = 0
    movimientos = movimientos_ia | movimientos_jugador
    centro = (Defines.GRID_NUM // 2, Defines.GRID_NUM // 2)

    for movimiento in movimientos:
        for pos in movimiento.positions:
            if board[pos.x][pos.y] == color_ia:
                distancia_al_centro = abs(pos.x - centro[0]) + abs(pos.y - centro[1])
                puntuacion += 10 - distancia_al_centro
            if board[pos.x][pos.y] == color_jugador:
                distancia_al_centro = abs(pos.x - centro[0]) + abs(pos.y - centro[1])
                puntuacion -= 10 - distancia_al_centro
    return puntuacion

def evaluar_espacios_libres(board, color):
    puntuacion = 0
    for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        for fila in range(Defines.GRID_NUM):
            for col in range(Defines.GRID_NUM):
                count_fichas = 0
                count_vacio = 0
                for i in range(6):  # Alinear hasta 6 fichas
                    nueva_fila = fila + i * dx
                    nueva_col = col + i * dy
                    if 0 <= nueva_fila < len(board) and 0 <= nueva_col < len(board[0]):
                        if board[nueva_fila][nueva_col] == color:
                            count_fichas += 1
                        elif board[nueva_fila][nueva_col] == Defines.NOSTONE:
                            count_vacio += 1
                if count_fichas > 0 and count_vacio > 0:
                    puntuacion += count_vacio * 10  # Mayor cantidad de espacios vacíos, más puntos
                if count_fichas > 0 and count_vacio == 0:
                    puntuacion -= 10  # Penalizar si el espacio está completamente bloqueado
    return puntuacion

def evaluar_bloqueo(board, color_ia, color_jugador, movimientos_ia, movimientos_jugador):
    puntuacion = 0
    movimientos = movimientos_ia | movimientos_jugador

    for direccion in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        for movimiento in movimientos:
            for pos in movimiento:
                count = 0
                for i in range(6):
                    nueva_fila= pos.x + i * direccion[0]
                    nueva_col = pos.y + i * direccion[1]
                    if 0 <= nueva_fila < len(board) and 0 <= nueva_col < len(board[0]):
                        if board[nueva_fila][nueva_col] == color_ia:
                            count += 1
                        if board[nueva_fila][nueva_col] == color_jugador:
                            count -= 1
                if count == 5:
                    if board[nueva_fila][nueva_col] == color_ia:
                        puntuacion += 100
                    if board[nueva_fila][nueva_col] == color_jugador:
                        puntuacion -= 100
                elif count == 4:
                    if board[nueva_fila][nueva_col] == color_ia:
                        puntuacion += 50
                    if board[nueva_fila][nueva_col] == color_jugador:
                        puntuacion -= 50
    return puntuacion

"""def evaluar(board, color_ia, color_jugador):
    puntuacion = 0
    centro = (Defines.GRID_NUM // 2, Defines.GRID_NUM // 2)

    for fila in range(Defines.GRID_NUM):
        for col in range(Defines.GRID_NUM):
            if board[fila][col] == color_ia:
                distancia_al_centro = abs(fila - centro[0]) + abs(col - centro[1])
                puntuacion += 10 - distancia_al_centro
            if board[fila][col] == color_jugador:
                distancia_al_centro = abs(fila - centro[0]) + abs(col - centro[1])
                puntuacion -= 10 - distancia_al_centro
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count_fichas = 0
                count_vacio = 0
                count_bloqueo = 0
                consecutivas_ia = 0
                consecutivas_jugador = 0
                for i in range(6):
                    nueva_fila = fila + i * dx
                    nueva_col = col + i * dy
                    if 0 <= nueva_fila < len(board) and 0 <= nueva_col < len(board[0]):
                        if board[nueva_fila][nueva_col] == color_ia:
                            count_fichas += 1
                            count_bloqueo += 1
                            consecutivas_ia += 1
                        if board[nueva_fila][nueva_col] == Defines.NOSTONE:
                            count_vacio += 1    
                        if board[nueva_fila][nueva_col] == color_jugador:
                            count_bloqueo -= 1
                            consecutivas_jugador += 1
                puntuacion += 2 ** (consecutivas_ia - 1) * 10
                puntuacion -= 2 ** (consecutivas_jugador - 1) * 10
                if count_bloqueo == 5:
                    if board[nueva_fila][nueva_col] == color_ia:
                        puntuacion += 100
                    if board[nueva_fila][nueva_col] == color_jugador:
                        puntuacion -= 100
                elif count_bloqueo == 4:
                    if board[nueva_fila][nueva_col] == color_ia:
                        puntuacion += 50
                    if board[nueva_fila][nueva_col] == color_jugador:
                        puntuacion -= 50
                if count_fichas > 0 and count_vacio > 0:
                    puntuacion += count_vacio * 10  # Mayor cantidad de espacios vacíos, más puntos
                if count_fichas > 0 and count_vacio == 0:
                    puntuacion -= 10  # Penalizar si el espacio está completamente bloqueado
    return puntuacion"""

def evaluar(board, color_ia, color_jugador):
    puntuacion = 0
    centro = (Defines.GRID_NUM // 2, Defines.GRID_NUM // 2)

    for fila in range(Defines.GRID_NUM):
        for col in range(Defines.GRID_NUM):
            if board[fila][col] == color_ia:
                distancia_al_centro = abs(fila - centro[0]) + abs(col - centro[1])
                puntuacion += 10 - distancia_al_centro
            if board[fila][col] == color_jugador:
                distancia_al_centro = abs(fila - centro[0]) + abs(col - centro[1])
                puntuacion -= 10 - distancia_al_centro

            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count_fichas = 0
                count_vacio = 0
                count_bloqueo = 0
                consecutivas_ia = 0
                consecutivas_jugador = 0

                for i in range(6):
                    nueva_fila = fila + i * dx
                    nueva_col = col + i * dy
                    if  0 <= nueva_fila < Defines.GRID_NUM and 0 <= nueva_col < Defines.GRID_NUM:
                        if board[nueva_fila][nueva_col] == color_ia:
                            count_fichas += 1
                            count_bloqueo += 1
                            consecutivas_ia += 1
                        if board[nueva_fila][nueva_col] == color_jugador:
                            count_bloqueo -= 1
                            consecutivas_jugador += 1
                        if board[nueva_fila][nueva_col] == Defines.NOSTONE:
                            count_vacio += 1    
                        
                puntuacion += ((2 ** (consecutivas_ia - 1)) - (2 ** (consecutivas_jugador - 1))) * 10
                if count_bloqueo == 5:
                    if board[nueva_fila][nueva_col] == color_ia:
                        puntuacion += 100
                    if board[nueva_fila][nueva_col] == color_jugador:
                        puntuacion -= 100
                elif count_bloqueo == 4:
                    if board[nueva_fila][nueva_col] == color_ia:
                        puntuacion += 50
                    if board[nueva_fila][nueva_col] == color_jugador:
                        puntuacion -= 50

                if count_fichas > 0:
                    puntuacion += (count_vacio * 10) if count_vacio > 0 else -10
    return puntuacion