from time import sleep
import random
from board import Board
from renderer import Renderer

class BoardInitializer:
    def __init__(self, init_type):
        if init_type == 'empty':
            self.call_method = self.empty_board
        elif init_type == 'random':
            self.call_method = self.random_board
        else:
            print('Method unknown')

    def empty_board(self, board):
        board.__init__(board.size)
        return board


    def random_board(self, board, n_moves=6):
        # Todo: Add clause to stop when the game is finished
        curr_color = board.next_turn
        for i in range(n_moves):
            avail_moves = board.enumerate_valid_moves(curr_color)

            if not avail_moves:
                return board
            rand_move = random.choice(avail_moves)
            board.make_move(*rand_move)
            curr_color = 'white' if curr_color == 'black' else 'black'

        return board

    def __call__(self, board):
        self.call_method(board)

if __name__ == '__main__':
    I = BoardInitializer('random')
    b = Board(4)
    I(b) 
    r = Renderer(512)
    r.draw_board(b)
    sleep(2)
