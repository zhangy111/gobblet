import copy
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
        init_board = copy.deepcopy(board)
        # Todo: Add clause to stop when the game is finished
        curr_color = board.next_turn
        for i in range(n_moves):
            avail_moves = board.enumerate_valid_moves(curr_color)
            if board.check_win_loss('white') != 'na':
                return self.random_board(init_board, n_moves)
            if not avail_moves:
                return board
            rand_move = random.choice(avail_moves)
            board.make_move(*rand_move)
            curr_color = 'white' if curr_color == 'black' else 'black'

        return board

    def __call__(self, board, *args, **kwargs):
        return self.call_method(board, *args, **kwargs)


def get_initial_board_states():
    b = Board(4)
    o = BoardInitializer('empty')
    r = BoardInitializer('random')

    opening_states = [o(copy.deepcopy(b)) for i in range(10)] # 3 Opening board states
    mid_game_states = [r(copy.deepcopy(b)) for i in range(30)] # 10 mid_game board states
    end_game_states = [r(copy.deepcopy(b), n_moves=30) for i in range(30)] # 10 mid_game board states

    # TODO
    # Need end-game states

    # return opening_states + mid_game_states
    # return opening_states
    # return mid_game_states
    # return end_game_states
    return opening_states

if __name__ == '__main__':
    l = get_initial_board_states()
    print(l)
