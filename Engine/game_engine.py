from defines import *
from tools import *
import sys
from search_engine import SearchEngine
import time
import copy

class GameEngine:
    def __init__(self, name=Defines.ENGINE_NAME):
        if name and len(name) > 0:
            if len(name) < Defines.MSG_LENGTH:
                self.m_engine_name = name
            else:
                print(f"Too long Engine Name: {name}, should be less than: {Defines.MSG_LENGTH}")
        self.m_alphabeta_depth = 6
        self.m_board = t = [ [0]*Defines.GRID_NUM for i in range(Defines.GRID_NUM)]
        self.init_game()
        self.m_search_engine = SearchEngine()
        self.m_best_move = StoneMove()
        self.m_chess_type = Defines.BLACK
        self.color_jugador = Defines.WHITE
        self.victoria = False
        self.movimientos = {}

    def init_game(self):
        init_board(self.m_board)

    def on_help(self):
        print(
            f"On help for GameEngine {self.m_engine_name}\n"
            " name        - print the name of the Game Engine.\n"
            " print       - print the board.\n"
            " exit/quit   - quit the game.\n"
            " black XXXX  - place the black stone on the position XXXX on the board.\n"
            " white XXXX  - place the white stone on the position XXXX on the board, X is from A to S.\n"
            " next        - the engine will search the move for the next step.\n"
            " move XXXX   - tell the engine that the opponent made the move XXXX,\n"
            "              and the engine will search the move for the next step.\n"
            " new black   - start a new game and set the engine to black player.\n"
            " new white   - start a new game and set it to white.\n"
            " depth d     - set the alpha beta search depth, default is 6.\n"
            " vcf         - set vcf search.\n"
            " unvcf       - set none vcf search.\n"
            " help        - print this help.\n")

    def run(self):
        msg = ""
        self.on_help()
        while True:
            msg = input().strip()
            log_to_file(msg)
            if msg == "name":
                print(f"name {self.m_engine_name}")
            elif msg == "exit" or msg == "quit":
                break
            elif msg == "print":
                print_board(self.m_board, self.m_best_move)
            elif msg == "vcf":
                self.m_vcf = True
            elif msg == "unvcf":
                self.m_vcf = False
            elif msg.startswith("black"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.m_best_move, Defines.BLACK)
                if self.color_jugador == Defines.BLACK:
                    move = copy.deepcopy(self.m_best_move)
                    self.movimientos[move.positions[0]] = -1
                    self.movimientos[move.positions[1]] = -1
                self.m_chess_type = Defines.BLACK
                """print("Jugador:")
                self.m_search_engine.print_jugador(self.movimientos)
                print("Ia")
                self.m_search_engine.print_ia(self.movimientos)"""
            elif msg.startswith("white"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.m_best_move, Defines.WHITE)
                if self.color_jugador == Defines.WHITE:
                    move = copy.deepcopy(self.m_best_move)
                    self.movimientos[move.positions[0]] = -1
                    self.movimientos[move.positions[1]] = -1
                self.m_chess_type = Defines.WHITE
                """print("Jugador:")
                self.m_search_engine.print_jugador(self.movimientos)
                print("Ia")
                self.m_search_engine.print_ia(self.movimientos)"""
            elif msg == "next":
                self.m_chess_type = self.m_chess_type ^ 3
                if self.search_a_move(self.m_chess_type, self.m_best_move):
                    msg = f"move {move2msg(self.m_best_move)}"
                    make_move(self.m_board, self.m_best_move, self.m_chess_type)
                    move = copy.deepcopy(self.m_best_move)
                    self.movimientos[move.positions[0]] = 1
                    self.movimientos[move.positions[1]] = 1
                    print(msg)
                    flush_output()
            elif msg.startswith("new"):
                self.init_game()
                self.movimientos = {}
                if msg[4:] == "black":
                    self.m_best_move = msg2move("JJ")
                    move = copy.deepcopy(self.m_best_move)
                    self.movimientos[move.positions[0]] = 1
                    make_move(self.m_board, self.m_best_move, Defines.BLACK)
                    self.m_chess_type = Defines.BLACK
                    self.color_jugador = Defines.WHITE
                    msg = "move JJ"
                    print(msg)
                    flush_output()
                else:
                    self.m_chess_type = Defines.WHITE
                    self.color_jugador = Defines.BLACK
            elif msg.startswith("move"):
                self.m_best_move = msg2move(msg[5:])
                move = copy.deepcopy(self.m_best_move)
                self.movimientos[move.positions[0]] = -1
                self.movimientos[move.positions[1]] = -1
                make_move(self.m_board, self.m_best_move, self.m_chess_type ^ 3)       
                if ver_victoria(self.m_board):
                    self.victoria = True
                    #print(f"Score:\t{self.m_search_engine.evaluacion(self.color_jugador, self.victoria)}")
                    print("Has ganado!")
                    break
                if self.search_a_move(self.m_chess_type, self.m_best_move):
                    msg = f"move {move2msg(self.m_best_move)}"
                    make_move(self.m_board, self.m_best_move, self.m_chess_type)
                    move = copy.deepcopy(self.m_best_move)
                    self.movimientos[move.positions[0]] = 1
                    self.movimientos[move.positions[1]] = 1
                    print(msg)
                    print_board(self.m_board, self.m_best_move)
                    flush_output()
                if is_win_by_premove(self.m_board, self.m_best_move):
                    self.victoria = True
                    #print(f"Score:\t{self.m_search_engine.evaluacion(self.color_ia, self.victoria)}")
                    print("Has perdido!")
                    break
            elif msg.startswith("depth"):
                d = int(msg[6:])
                if 0 < d < 10:
                    self.m_alphabeta_depth = d
                print(f"Set the search depth to {self.m_alphabeta_depth}.\n")
            elif msg == "help":
                self.on_help()
            """elif msg == "jugador":
                self.m_search_engine.print_jugador(self.movimientos)
            elif msg == "ia":
                self.m_search_engine.print_ia(self.movimientos)"""

        return 0

    def search_a_move(self, ourColor, bestMove):
        score = 0
        start = 0
        end = 0

        start = time.perf_counter()
        self.m_search_engine.before_search(self.m_board, self.m_chess_type, self.m_alphabeta_depth)
        score = self.m_search_engine.alpha_beta_search(self.m_alphabeta_depth, Defines.MININT, Defines.MAXINT, ourColor, bestMove, bestMove, self.movimientos)
        end = time.perf_counter()

        #score = self.m_search_engine.evaluacion(None, False, self.m_board)

        print(f"AB Time:\t{end - start:.3f}")
        print(f"Node:\t{self.m_search_engine.m_total_nodes}")
        print(f"Nodos podados:\t{self.m_search_engine.nodos_podados}\n")
        #print(f"Score:\t{score:.3f}")
        return True

def flush_output():
    sys.stdout.flush()


# Create an instance of GameEngine and run the game
if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()


"""elif msg.startswith("black"):
                print_board(self.m_board, self.m_best_move)
                if self.color_jugador == Defines.BLACK:
                    self.m_best_move = msg2move(msg[6:])
                    make_move(self.m_board, self.m_best_move, Defines.BLACK)
                    self.m_chess_type = Defines.BLACK
                else:
                    if self.search_a_move(self.m_chess_type, self.m_best_move):
                        msg = f"move {move2msg(self.m_best_move)}"
                        make_move(self.m_board, self.m_best_move, self.m_chess_type)
                        print(msg)
                        print_board(self.m_board, self.m_best_move)
                        flush_output()
            elif msg.startswith("white"):
                if self.color_jugador == Defines.WHITE:
                    print("Turno jugador")
                    self.m_best_move = msg2move(msg[6:])
                    print(f"movimiento: {self.m_best_move}")
                    make_move(self.m_board, self.m_best_move, Defines.WHITE)
                    print("Movimiento hecho")
                    self.m_chess_type = Defines.WHITE
                else:
                    if self.search_a_move(self.m_chess_type, self.m_best_move):
                        msg = f"move {move2msg(self.m_best_move)}"
                        make_move(self.m_board, self.m_best_move, self.m_chess_type)
                        print(msg)
                        print_board(self.m_board, self.m_best_move)
                        flush_output()"""