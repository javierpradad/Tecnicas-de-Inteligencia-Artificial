from tools import *
import random

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
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


    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
    
        #Check game result
        if (is_win_by_premove(self.m_board, preMove)):
            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return 0;
            else:
                #Self wins.
                return Defines.MININT + 1;
        
        alpha = 0
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10
        else:   
            move1 = self.find_possible_move(self.m_alphabeta_depth)
            bestMove.positions[0].x = move1[0]
            bestMove.positions[0].y = move1[1]
            bestMove.positions[1].x = move1[0]
            bestMove.positions[1].y = move1[1]
            make_move(self.m_board,bestMove,ourColor)
            
            '''Check game result
            if (is_win_by_premove(self.m_board, bestMove)):
                #Self wins.
                return Defines.MININT + 1;'''
            
            move2 = self.find_possible_move(self.m_alphabeta_depth)
            bestMove.positions[1].x = move2[0]
            bestMove.positions[1].y = move2[1]
            make_move(self.m_board,bestMove,ourColor)

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
    
    def buscar_candidatos(self, board):
        candidatos = set()
        direcciones = [(1, 0), (0, 1), (1, 1), (1, -1)]
        max_candidatos = 10

        for fila in range(Defines.GRID_NUM):
            for col in range(Defines.GRID_NUM):
                if board[fila][col] == self.color_ia:
                    for dx, dy in direcciones:
                        nueva_fila = fila + dx
                        nueva_col = col + dy
                        if (0 <= nueva_fila < Defines.GRID_NUM) and (0 <= nueva_col < Defines.GRID_NUM):
                            if board[nueva_fila][nueva_col] == Defines.NOSTONE:
                                candidatos.add((nueva_fila, nueva_col))

        candidatos = list(candidatos)
        if len(candidatos) > max_candidatos:
            candidatos = random.sample(candidatos, max_candidatos)

        return candidatos
    
    def evaluacion(self, ganador=None, victoria=False, board=None):
        if victoria:
            if ganador == self.color_ia:
                return Defines.MAXINT
            elif ganador == self.color_jugador:
                return Defines.MININT
            elif ver_empate(board):
                return self.DRAW_SCORE

        puntuacion = 0   

        puntuacion += contar_piedras(self.color_ia, board) * 10 
        puntuacion -= contar_piedras(self.color_jugador, board) * 10

        return puntuacion
    
    def min_max(self, board, depth, alpha, beta, maximizando):
        victoria = ver_victoria(board)
        empate = ver_empate(board)

        if depth > 2:
            depth = 2

        if depth == 0 or victoria or empate:
            if victoria:
                ganador = self.color_jugador if not maximizando else self.color_ia
                return self.evaluacion(ganador=ganador, victoria=True, board=board)
            elif empate:
                return self.evaluacion(ganador=None, victoria=True, board=board)
            return self.evaluacion(ganador=None, victoria=False, board=board)
        
        mejor_puntuacion = -float('inf') if maximizando else float('inf')
        movimientos = self.buscar_candidatos(board)

        for i, movimiento1 in enumerate(movimientos):
            for j, movimiento2 in enumerate(movimientos):
                if i == j:
                    continue  # No permitimos poner dos fichas en la misma posición
            
            # Simular el primer movimiento
                tablero_aux = self.simular_movimiento(board, movimiento1, self.color_ia if maximizando else self.color_jugador)
            # Simular el segundo movimiento
                tablero_aux = self.simular_movimiento(tablero_aux, movimiento2, self.color_ia if maximizando else self.color_jugador)
                puntuacion = self.min_max(tablero_aux, depth - 1, alpha, beta, not maximizando)

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

        return mejor_puntuacion
    
    def find_possible_move(self, depth):
        mejor_puntuacion = -float('inf')
        mejor_movimiento = None
        alpha = -float('inf')
        beta = float('inf')

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

        return mejor_movimiento
    
    def simular_movimiento(self, board, movimiento, color):
        fila, col = movimiento
        tablero_aux = [fila[:] for fila in board]  # Hacemos una copia profunda del tablero
        tablero_aux[fila][col] = color  # Realizamos el movimiento en la copia
        return tablero_aux

    

def flush_output():
    import sys
    sys.stdout.flush()
