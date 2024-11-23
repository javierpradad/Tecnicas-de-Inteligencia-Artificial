from tools import *

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0
        self.color_ia = None
        self.color_jugador = None

    def before_search(self, board, color_ia, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0
        self.color_ia = color_ia
        self.color_jugador = Defines.BLACK if self.color_ia == Defines.WHITE else Defines.WHITE


    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove, movimientos):
    
        #Check game result
        if (is_win_by_premove(self.m_board, preMove)):
            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return Defines.MININT
            else:
                #Self wins.
                return Defines.MININT + 1
        
        alpha = 0
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10
        else:   
            move1, move2 = self.find_possible_move(self.m_alphabeta_depth, movimientos)
            bestMove.positions[0].x = move1[0]
            bestMove.positions[0].y = move1[1]
            bestMove.positions[1].x = move2[0]
            bestMove.positions[1].y = move2[1]
            make_move(self.m_board, bestMove, ourColor, movimientos)

        return alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
    
    def buscar_candidatos(self, board, movimientos):
        ofensivos = set()
        defensivos = set()
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]

        #Recorrer la lista de movimientos
        for movimiento, jugador in movimientos.items():
            for dx, dy in direcciones:
                for dist in range(1, 3): #Ver en una distancia de uno a 3 espacios
                    nueva_fila = movimiento.x + dx * dist
                    nueva_col = movimiento.y + dy * dist
                    if isValidPos(nueva_fila, nueva_col) and board[nueva_fila][nueva_col] == Defines.NOSTONE:
                        if jugador == self.color_jugador:
                            defensivos.add((nueva_fila, nueva_col))
                        if jugador == self.color_ia: 
                            ofensivos.add((nueva_fila, nueva_col))
                    nueva_fila = movimiento.x + -dx * dist
                    nueva_col = movimiento.y + -dy * dist
                    if isValidPos(nueva_fila, nueva_col) and board[nueva_fila][nueva_col] == Defines.NOSTONE: #Añadir la direccion contraria
                        if jugador == self.color_jugador:
                            defensivos.add((nueva_fila, nueva_col))
                        if jugador == self.color_ia: 
                            ofensivos.add((nueva_fila, nueva_col))
                            
        #Ordenar en funcion de la puntuacion y devolver los cuatro mejores
        ofensivos = sorted(ofensivos, key=lambda pos: self.evaluar_posicion(pos, board, self.color_ia), reverse=True) 
        defensivos = sorted(defensivos, key=lambda pos: self.evaluar_posicion(pos, board, self.color_jugador), reverse=True)
        candidatos_finales = ofensivos[:4] + defensivos[:4]
        return candidatos_finales

    def evaluar_posicion(self, posicion, board, color):
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]
        puntuacion = 0

        for dx, dy in direcciones:
            longitud = contar_cadena(board, posicion[0], posicion[1], dx, dy, color)
            longitud = contar_cadena(board, posicion[0], posicion[1], -dx, -dy, color)
            puntuacion += 2 ** longitud
        
        return puntuacion
    
    def evaluacion(self, ganador=None, victoria=False, board=None, movimientos={}):
        if victoria:
            if ganador == self.color_ia:
                return Defines.MAXINT
            elif ganador == self.color_jugador:
                return Defines.MININT
            elif ver_empate(board):
                return 0

        puntuacion = 0
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Evaluación de cadenas de ambos jugadores
        for movimiento, color in movimientos.items():
            for dx, dy in direcciones:
                longitud = contar_cadena(board, movimiento.x, movimiento.y, dx, dy, color)
                if color == self.color_ia:
                    puntuacion += 2 ** longitud
                else:
                    puntuacion -= 3 ** longitud  # Penaliza más al jugador

                if longitud == 4:  # Espacio clave para ganar
                    if color == self.color_ia:
                        puntuacion += 500
                    else:
                        puntuacion -= 800  # Penalización más alta
                if longitud == 5:  # Espacio clave para ganar
                    if color == self.color_ia:
                        puntuacion += 2000
                    else:
                        puntuacion -= 5000  # Penalización más alta

        # Bonus por proximidad al centro para la IA
        centro = Defines.GRID_NUM // 2
        for fila in range(1, Defines.GRID_NUM - 1):
            for col in range(1, Defines.GRID_NUM - 1):
                if board[fila][col] == self.color_ia:
                    puntuacion += max(0, 10 - abs(fila - centro) - abs(col - centro))
                elif board[fila][col] == self.color_jugador:
                    puntuacion -= max(0, 10 - abs(fila - centro) - abs(col - centro))

        return puntuacion
    
    def min_max(self, depth, alpha, beta, maximizando, movimientos, move):
        victoria = is_win_by_premove(self.m_board, move)
        empate = ver_empate(self.m_board)
        #Definir profundidad maxima
        if depth > 2:
            depth = 2

        #Criterios para devolver la puntuacion
        if depth == 0 or victoria or empate:
            if victoria:
                ganador = self.color_jugador if not maximizando else self.color_ia
                return self.evaluacion(ganador=ganador, victoria=True, board=self.m_board, movimientos=movimientos)
            elif empate:
                return self.evaluacion(ganador=None, victoria=True, board=self.m_board, movimientos=movimientos)
            return self.evaluacion(ganador=None, victoria=False, board=self.m_board, movimientos=movimientos)
        
        mejor_puntuacion = Defines.MININT if maximizando else Defines.MAXINT
        candidatos = self.buscar_candidatos(self.m_board, movimientos)

        for i, movimiento1 in enumerate(candidatos):
            for j, movimiento2 in enumerate(candidatos):
                if i == j:
                    continue  #No permitimos poner dos fichas en la misma posición
                
                movimiento = StoneMove()
                movimiento.positions[0].x = movimiento1[0]
                movimiento.positions[0].y = movimiento1[1]
                movimiento.positions[1].x = movimiento2[0]
                movimiento.positions[1].y = movimiento2[1]
                make_move(self.m_board, movimiento, self.color_ia if maximizando else self.color_jugador, movimientos) #Simular movimiento
                puntuacion = self.min_max(depth - 1, alpha, beta, not maximizando, movimientos, movimiento)
                unmake_move(self.m_board, movimiento, movimientos)

                if maximizando:
                    mejor_puntuacion = max(mejor_puntuacion, puntuacion)
                    alpha = max(alpha, puntuacion)
                    if beta <= alpha:
                        break
                else:
                    mejor_puntuacion = min(mejor_puntuacion, puntuacion)
                    beta = min(beta, puntuacion)
                    if beta <= alpha:
                        break

        return mejor_puntuacion
    
    def find_possible_move(self, depth, movimientos):
        mejor_puntuacion = Defines.MININT
        mejor_movimiento1 = None
        mejor_movimiento2 = None
        alpha = Defines.MININT
        beta = Defines.MAXINT
        candidatos = self.buscar_candidatos(self.m_board, movimientos)

        #Recorrer los movimietnos
        for i, movimiento1 in enumerate(candidatos):
            for j, movimiento2 in enumerate(candidatos):
                if i == j:
                    continue # No permitimos poner dos fichas en la misma posición
                
                movimiento = StoneMove()
                movimiento.positions[0].x = movimiento1[0]
                movimiento.positions[0].y = movimiento1[1]
                movimiento.positions[1].x = movimiento2[0]
                movimiento.positions[1].y = movimiento2[1]
                make_move(self.m_board, movimiento, self.color_ia, movimientos) #Simular movimiento

                if is_win_by_premove(self.m_board, movimiento):
                    unmake_move(self.m_board, movimiento, movimientos)
                    return movimiento1, movimiento2
                    
                puntuacion = self.min_max(depth - 1, alpha, beta, False, movimientos, movimiento)  #El oponente tratará de minimizar
                unmake_move(self.m_board, movimiento, movimientos) #Deshacer la simulación
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_movimiento1 = movimiento1
                    mejor_movimiento2 = movimiento2
                alpha = max(alpha, puntuacion)  #Actualizar alpha aquí también

                if beta <= alpha:
                    break

        return mejor_movimiento1, mejor_movimiento2
    
    def print_jugador(self, movimientos):
        for movimiento, jugador in movimientos.items():
            if jugador == self.color_jugador:
                print(f"{movimiento.x}, {movimiento.y}")

    def print_ia(self, movimientos):
        for movimiento, jugador in movimientos.items():
            if jugador == self.color_ia:
                print(f"{movimiento.x}, {movimiento.y}")

    def print_cadenas(self, movimientos):
        cadena_j = 0
        cadena_ia = 0
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for movimiento, jugador in movimientos.items():
            for dx, dy in direcciones:
                longitud = contar_cadena(self.m_board, movimiento.x, movimiento.y, dx, dy, jugador)
                if jugador == self.color_jugador:
                    if longitud > cadena_j:
                        cadena_j = longitud
                if jugador == self.color_ia:
                    if longitud > cadena_ia:
                        cadena_ia = longitud
        
        print(f"Cadena más larga de la IA: {cadena_ia}")
        print(f"Cadena más larga del jugadir: {cadena_j}")
    

def flush_output():
    import sys
    sys.stdout.flush()