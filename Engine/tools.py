from defines import *
import time
import copy

# Point (x, y) if in the valid position of the board.
def isValidPos(x,y):
    return x>0 and x<Defines.GRID_NUM-1 and y>0 and y<Defines.GRID_NUM-1
    
def init_board(board):
    for i in range(21):
        board[i][0] = board[0][i] = board[i][Defines.GRID_NUM - 1] = board[Defines.GRID_NUM - 1][i] = Defines.BORDER
    for i in range(1, Defines.GRID_NUM - 1):
        for j in range(1, Defines.GRID_NUM - 1):
            board[i][j] = Defines.NOSTONE
            
def make_move(board, move, color, movimientos):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color
    movimiento = copy.deepcopy(move)
    movimientos[movimiento.positions[0]] = color
    movimientos[movimiento.positions[1]] = color
    

def unmake_move(board, move, movimientos):
    board[move.positions[0].x][move.positions[0].y] = Defines.NOSTONE
    board[move.positions[1].x][move.positions[1].y] = Defines.NOSTONE
    if move.positions[0] in movimientos:
        del movimientos[move.positions[0]]
    if move.positions[1] in movimientos:
        del movimientos[move.positions[1]]

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
    # Iterar sobre todo el tablero
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
                count += contar_cadena(board, fila, col, dx, dy, color_actual) 
                #print(f"segundo count: {count}")
                count += contar_cadena(board, fila, col, -dx, -dy, color_actual) 
                #print(f"tercer count: {count}")
                #print("-----------------------------------------------------------------------")
                if count >= 6:
                    return True
            
    return False

def ver_empate(board):
    if board == None:
        return False
    #Recorrer todas las filas en busca de una casilla vacia
    for fila in board:
        if Defines.NOSTONE in fila:
            return False
    return True

def contar_piedras(color, board):
    piedras = 0
    direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]

    #Recorrer todo el tablero
    for fila in range(1, Defines.GRID_NUM - 1):
        for col in range(1, Defines.GRID_NUM - 1):
            if board[fila][col] == color:
                #Contar piedras en todas las direcciones
                for dx, dy in direcciones:
                    longitud_cadena = contar_cadena(board, fila, col, dx, dy, color)
                    if longitud_cadena > 1:
                        piedras += 2 ** (longitud_cadena - 1)

    return piedras
    
def contar_cadena(board, fila, col, dx, dy, color):
    consecutivas = 1
    n = len(board)

    #Ver en un rango de una a 6 casillas si hay cadena
    for i in range(1, 6):
        nueva_fila = fila + i * dx
        nueva_col = col + i * dy

        #Parar en caso de que se salga del tablero
        if nueva_fila < 0 or nueva_fila >= n or nueva_col < 0 or nueva_col >= n:
            break

        if board[nueva_fila][nueva_col] == color:
            consecutivas += 1
        else:
            break

    return consecutivas

def distancia_heuristica(pos, movimientos):
    # Calcula la distancia heurística de una posición a todas las fichas en juego
    return min(abs(pos[0] - move.x) + abs(pos[1] - move.y) for move in movimientos.keys())

