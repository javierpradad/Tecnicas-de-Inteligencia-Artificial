from tools import *
import random
import copy

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0
        self.nodos_podados = 0
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
        if preMove and is_win_by_premove(self.m_board, preMove):
            if (ourColor == self.color_ia):
                #Opponent wins.
                return 0
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
            move = self.find_possible_move(self.m_alphabeta_depth, movimientos)
            bestMove.positions[0].x = move.positions[0].x
            bestMove.positions[0].y = move.positions[0].y
            bestMove.positions[1].x = move.positions[1].x
            bestMove.positions[1].y = move.positions[1].y
            make_move(self.m_board,bestMove,ourColor)
            print(f"movimiento final: {bestMove.positions[0].x}, {bestMove.positions[0].y} y {bestMove.positions[1].x}, {bestMove.positions[1].y}")
            '''Check game result
            if (is_win_by_premove(self.m_board, bestMove)):
                #Self wins.
                return Defines.MININT + 1;'''
            
            """move2 = self.find_possible_move(self.m_alphabeta_depth)
            bestMove.positions[1].x = move2[0]
            bestMove.positions[1].y = move2[1]"""
        return alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    """def find_possible_move(self):
        candidatos = self.buscar_candidatos()

        if candidatos:
            # Seleccionamos un candidato aleatorio de los encontrados
            return random.choice(candidatos)
        else:
            # Si no hay candidatos, buscar el primer espacio vacío
            for i in range(1, len(self.m_board) - 1):
                for j in range(1, len(self.m_board[i]) - 1):
                    if self.m_board[i][j] == Defines.NOSTONE:
                        return (i, j)
        
        return (-1, -1)"""
    
    """def buscar_candidatos(self):
            candidatos = set()
            direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]
            max_candidatos = 10

            movimientos_totales = self.movimientos_ia | self.movimientos_jugador

            for move in movimientos_totales:
                for pos in move.positions:
                    for dx, dy in direcciones:
                        nueva_fila = pos.x + dx
                        nueva_col = pos.y + dy
                        if (0 <= nueva_fila < Defines.GRID_NUM) and (0 <= nueva_col < Defines.GRID_NUM):
                            if self.m_board[nueva_fila][nueva_col] == Defines.NOSTONE:
                                movimiento = StonePosition(nueva_fila, nueva_col)
                                candidatos.add((movimiento))

            candidatos = list(candidatos)
            if len(candidatos) > max_candidatos:
                candidatos = random.sample(candidatos, max_candidatos)
            
            return candidatos"""

    def buscar_candidatos(self, maximizando, movimientos):
        candidatos_bloqueo = set()
        candidatos_cadena = set()
        candidatos = set()
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]
        mejor_movimiento = StoneMove()
        mejor_movimiento.score = Defines.MININT
        max_candidatos = 10

        movimientos_ia = set()
        movimientos_jugador = set()

        for move, jugador in movimientos.items():
            if jugador == 1:
                movimientos_ia.add(move)
            else:
                movimientos_jugador.add(move)
        

        for move, jugador in movimientos.items():
            for dx, dy in direcciones:
                nueva_fila = move.x + dx
                nueva_col = move.y + dy
                nueva_fila_n = move.x + dx * -1
                nueva_col_n = move.y + dy * -1
                if isValidPos(nueva_fila, nueva_col):
                    if self.m_board[nueva_fila][nueva_col] == Defines.NOSTONE:
                        movimiento = StonePosition(nueva_fila, nueva_col)
                        if jugador == 1:
                            candidatos_cadena.add((movimiento))
                        else:
                            candidatos_bloqueo.add((movimiento))
                if isValidPos(nueva_fila, nueva_col):
                    if self.m_board[nueva_fila_n][nueva_col_n] == Defines.NOSTONE:
                        movimiento = StonePosition(nueva_fila_n, nueva_col_n)
                        if jugador == 1:
                            candidatos_cadena.add((movimiento))
                        else:
                            candidatos_bloqueo.add((movimiento))

        for movimiento_cadena in candidatos_cadena:
            for movimiento_bloqueo in candidatos_bloqueo:
                movimiento = StoneMove()
                movimiento.positions = [movimiento_cadena, movimiento_bloqueo]
                if maximizando:
                    movimiento.score = evaluar_movimiento(movimiento, movimientos_ia, movimientos_jugador)
                else:
                    movimiento.score = evaluar_movimiento(movimiento, movimientos_jugador, movimientos_ia)
                candidatos.add(movimiento)

        if len(candidatos) > max_candidatos:
            candidatos = sorted(candidatos, key=lambda movimiento: movimiento.score, reverse=True)[:max_candidatos]

        while len(candidatos) <= 0:
            movimiento = StoneMove()
            movimiento.positions[0].x = 6
            movimiento.positions[0].y = 6
            movimiento.positions[1].x = 5
            movimiento.positions[1].y = 5
            movimiento.score = evaluar_movimiento(movimiento, movimientos_ia, movimientos_jugador)
            if movimiento.positions[0].x != movimiento.positions[1].x  and movimiento.positions[0].y != movimiento.positions[1].y:
                if self.m_board[movimiento.positions[0].x][movimiento.positions[0].y] == Defines.NOSTONE and self.m_board[movimiento.positions[0].x][movimiento.positions[0].y] == Defines.NOSTONE:
                    candidatos.add(movimiento)
        return candidatos

    """def buscar_candidatos(self, board):
        candidatos = set()
        max_candidatos = 10
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, 1), (-1, -1)]

        def buscar_amenazas():
            for fila in range(Defines.GRID_NUM):
                for col in range(Defines.GRID_NUM):
                    if len(candidatos) > max_candidatos:
                        break
                    if board[fila][col] == self.color_jugador:
                        for dx, dy in direcciones:
                            cadena = contar_cadena(board, fila, col, dx, dy, self.color_jugador)
                            nueva_fila = fila + cadena * dx
                            nueva_col = col + cadena * dy
                            if cadena >= 4 and (0 <= nueva_fila < Defines.GRID_NUM) and (0 <= nueva_col < Defines.GRID_NUM):
                                if board[nueva_fila][nueva_col] == Defines.NOSTONE:
                                    candidatos.add((nueva_fila, nueva_col))

        def buscar_oportunidades():
            for fila in range(Defines.GRID_NUM):
                for col in range(Defines.GRID_NUM):
                    if len(candidatos) > max_candidatos:
                        break
                    if board[fila][col] == self.color_ia:
                        for dx, dy in direcciones:
                            nueva_fila = fila + dx
                            nueva_col = col + dy
                            if (0 <= nueva_fila < Defines.GRID_NUM) and (0 <= nueva_col < Defines.GRID_NUM):
                                if board[nueva_fila][nueva_col] == Defines.NOSTONE:
                                    candidatos.add((nueva_fila, nueva_col))
        
        buscar_amenazas()
        if  len(candidatos) < max_candidatos:
            buscar_oportunidades()

        while len(candidatos) <= 0:
            nueva_fila = random.randint(0, Defines.GRID_NUM-1)
            nueva_col = random.randint(0, Defines.GRID_NUM-1)
            if board[nueva_fila][nueva_col] == Defines.NOSTONE:
                candidatos.add((nueva_fila, nueva_col))
        
        return candidatos"""
    
    """def evaluacion(self, ganador=None, victoria=False):
        if victoria:
            if ganador == self.color_ia:
                return Defines.MAXINT
            elif ganador == self.color_jugador:
                return Defines.MININT
            elif ver_empate(self.m_board):
                return self.DRAW_SCORE

        puntuacion = 0

        puntuacion += contar_piedras(self.color_ia, self.m_board, self.color_jugador, self.movimientos_ia, self.movimientos_jugador) * 10 
        puntuacion -= contar_piedras(self.color_jugador, self.m_board, self.color_jugador, self.movimientos_ia, self.movimientos_jugador) * 10

        return puntuacion"""
    
    def min_max(self, depth, alpha, beta, maximizando, movimientos):
        self.m_total_nodes += 1
        victoria = ver_victoria(self.m_board)
        if not victoria:
            empate = ver_empate(self.m_board)

        if depth > 2:
            depth = 2

        if depth == 0 or victoria or empate:
            if victoria:
                return Defines.MININT if maximizando else Defines.MAXINT #Ha ganado el jugador del turno anterior
            elif empate:
                return 0
            return evaluar(self.m_board, self.color_ia, self.color_jugador)
        mejor_puntuacion = Defines.MININT if maximizando else Defines.MAXINT
        candidatos = self.buscar_candidatos(maximizando, movimientos)

        for movimiento in candidatos:
            make_move(self.m_board, movimiento, self.color_ia if maximizando else self.color_jugador)
            if maximizando:
                movimientos[movimiento.positions[0]] = 1
                movimientos[movimiento.positions[1]] = 1
            else:
                movimientos[movimiento.positions[0]] = -1
                movimientos[movimiento.positions[1]] = -1
                #self.print_jugador()
            puntuacion = self.min_max(depth - 1, alpha, beta, not maximizando, movimientos)
            movimiento.score = combinar_evaluaciones(puntuacion, movimiento.score)
            unmake_move(self.m_board, movimiento)
            del movimientos[movimiento.positions[0]]
            del movimientos[movimiento.positions[1]]

            #print(f"Puntuación: {puntuacion}")
            #print("------------------------------------------------------------------")

            if maximizando:
                mejor_puntuacion = max(mejor_puntuacion, movimiento.score)
                alpha = max(alpha, movimiento.score)
                if beta <= alpha:
                    self.nodos_podados += 1
                    break
            else:
                mejor_puntuacion = min(mejor_puntuacion, movimiento.score)
                beta = min(beta, movimiento.score)
                if beta <= alpha:
                    self.nodos_podados += 1
                    break

        return mejor_puntuacion


    """def min_max(self, board, depth, alpha, beta, maximizando, movimientos_ia_aux, movimientos_jugador_aux):

        victoria = ver_victoria(board)
        if not victoria:
            empate = ver_empate(board)

        if depth > 2:
            depth = 2

        if depth == 0 or victoria or empate:
            if victoria:
                ganador = self.color_jugador if not maximizando else self.color_ia
                return self.evaluacion(ganador=ganador, victoria=True, board=board, movimientos_ia=movimientos_ia_aux, movimientos_jugador=movimientos_jugador_aux)
            elif empate:
                return self.evaluacion(ganador=None, victoria=True, board=board, movimientos_ia=movimientos_ia_aux, movimientos_jugador=movimientos_jugador_aux)
            return self.evaluacion(ganador=None, victoria=False, board=board, movimientos_ia=movimientos_ia_aux, movimientos_jugador=movimientos_jugador_aux)
        
        mejor_puntuacion = Defines.MININT if maximizando else Defines.MAXINT
        movimientos = self.buscar_candidatos(board, movimientos_ia_aux, movimientos_jugador_aux)

        for i, movimiento1 in enumerate(movimientos):
            for j, movimiento2 in enumerate(movimientos):
                if i == j:
                    continue  # No permitimos poner dos fichas en la misma posición
            
                tablero_aux = self.simular_movimientos(board, movimiento1, movimiento2, self.color_ia if maximizando else self.color_jugador)
                movimiento = StoneMove()
                movimiento.positions[0] = movimiento1
                movimiento.positions[1] = movimiento2
                if maximizando:
                    movimientos_ia_aux.append(movimiento)
                else:
                    movimientos_jugador_aux.append(movimiento)
                puntuacion = self.min_max(tablero_aux, depth - 1, alpha, beta, not maximizando, movimientos_ia_aux, movimientos_jugador_aux)

                #print(f"Puntuación: {puntuacion}")
                #print("------------------------------------------------------------------")

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

        return mejor_puntuacion"""
    
    """def find_possible_move(self, depth):
        mejor_puntuacion = Defines.MININT
        mejor_movimiento = None
        alpha = Defines.MININT
        beta = Defines.MAXINT

        for movimiento in self.buscar_candidatos(self.m_board):
            tablero_aux = self.simular_movimiento(self.m_board, movimiento, self.color_ia)

            if ver_victoria(tablero_aux):
                return movimiento
                
            puntuacion = self.min_max(tablero_aux, depth - 1, alpha, beta, False)  # El oponente tratará de minimizar
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_movimiento = movimiento
            alpha = max(alpha, puntuacion)  # Actualizar alpha aquí también

            if beta <= alpha:
                break

        return mejor_movimiento"""
    
    def find_possible_move(self, depth, movimientos):
        mejor_movimiento = StoneMove()
        alpha = Defines.MININT
        beta = Defines.MAXINT
        self.m_total_nodes = 0
        self.nodos_podados = 0

        candidatos = self.buscar_candidatos(True, movimientos)
        for movimiento in candidatos:

            if is_win_by_premove(self.m_board, movimiento):
                mejor_movimiento = movimiento
                mejor_movimiento.score = Defines.MAXINT
                return mejor_movimiento
            
            make_move(self.m_board, movimiento, self.color_ia)
            movimiento.score = self.min_max(depth - 1, alpha, beta, False, movimientos)  # El oponente tratará de minimizar
            if movimiento.score > mejor_movimiento.score:
                mejor_movimiento = movimiento
            alpha = max(alpha, movimiento.score)  # Actualizar alpha aquí también

            unmake_move(self.m_board, movimiento)
            if beta <= alpha:
                break

        return mejor_movimiento
    
    """def find_possible_move(self, depth):
        mejor_movimiento = StoneMove()
        alpha = Defines.MININT
        beta = Defines.MAXINT
        
        movimientos = self.buscar_candidatos()
        for i, mov1 in enumerate(movimientos):
            for j, mov2 in enumerate(movimientos):
                if i == j:
                    continue
            
            movimiento = StoneMove()
            movimiento.positions[0] = mov1
            movimiento.positions[1] = mov2

            if is_win_by_premove(self.m_board, movimiento):
                mejor_movimiento.positions[0] = StonePosition(mov1.x, mov1.y)
                mejor_movimiento.positions[1] = StonePosition(mov2.x, mov2.y)
                mejor_movimiento.score = Defines.MAXINT
                return mejor_movimiento
            
            make_move(self.m_board, movimiento, self.color_ia)
            movimiento.score = self.min_max(depth - 1, alpha, beta, False)  # El oponente tratará de minimizar
            if movimiento.score > mejor_movimiento.score:
                mejor_movimiento.positions[0] = StonePosition(mov1.x, mov1.y)
                mejor_movimiento.positions[1] = StonePosition(mov2.x, mov2.y)
                mejor_movimiento.score = movimiento.score
            alpha = max(alpha, movimiento.score)  # Actualizar alpha aquí también

            unmake_move(self.m_board, movimiento)
            if beta <= alpha:
                break

        return mejor_movimiento"""
    
    """def simular_movimiento(self, board, movimiento, color):
        fila, col = movimiento
        tablero_aux = [fila[:] for fila in board]  # Hacemos una copia profunda del tablero
        tablero_aux[fila][col] = color  # Realizamos el movimiento en la copia
        return tablero_aux"""
    
    """def simular_movimientos(self, board, movimiento1, movimiento2, color):
        tablero_aux = [fila[:] for fila in board]  # Hacemos una copia profunda del tablero
        tablero_aux[movimiento1.x][movimiento1.y] = color  # Realizamos el movimiento en la copia
        tablero_aux[movimiento2.x][movimiento2.y] = color
        return tablero_aux"""

    def print_jugador(self, movimientos):
        for movimiento in movimientos:
                print(f"{movimiento.positions[0].x}, {movimiento.positions[0].y} y {movimiento.positions[1].x}, {movimiento.positions[1].y}")

    def print_ia(self, movimientos):
        for movimiento in movimientos:
                print(f"{movimiento.positions[0].x}, {movimiento.positions[0].y} y {movimiento.positions[1].x}, {movimiento.positions[1].y}")

def flush_output():
    import sys
    sys.stdout.flush()
