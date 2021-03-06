import pygame
import numpy as np
from time import sleep
from renderer import Renderer


class Board:
    free_pieces = None
    size = 0

    def __init__(self, board_size=4):
        '''
        Set up the board and initialize every space to None
        Pre-condition: board_size > 0
        Post-condition: board and free_pieces initialized
        '''
        self.board = None

        rows = [i for i in range(1, board_size+1)]
        cols = [j for j in range(1, board_size+1)]  # could also use letters
        spaces = [(r, c) for r in rows for c in cols]

        # A 1D dict with each a stack of pieces for each "space"
        self.board = dict(zip(spaces, [[] for k in range(board_size ** 2)]))

        # Side stacks are stacks provided to each player at the beginning of the game

        # {(0, 1): [('white', 1), ('white', 2), ('white', 3), ('white', 4)], (0, 2): [('white', 1): ...]
        # {(N+1, 1): [('black', 1), ('black', 2), ('black', 3), ('black', 4)], (0, 2): [('black', 1): ...]
        white_side_stacks = dict(zip([(0, j) for j in [1, 2, 3]], [
                                 [('white', size) for size in [1, 2, 3, 4]] for k in range(3)]))
        black_side_stacks = dict(zip([(board_size+1, j) for j in [1, 2, 3]], [
                                 [('black', size) for size in [1, 2, 3, 4]] for k in range(3)]))

        # Each move now can be represented as a tuple: (i, j) -> (k, l)
        # i.e. move piece from top of (i, j) to (k, l)

        self.board.update(white_side_stacks)
        self.board.update(black_side_stacks)
        self.size = board_size
        
        self.next_turn = 'white' # Next player's color

        # memory to check win-loss quickly
        self.white_board = np.zeros([self.size, self.size])
        self.black_board = np.zeros([self.size, self.size])

        print("Welcome to Gobblet.")

    def can_move(self, old_pos, new_pos):
        if old_pos not in self.board or new_pos not in self.board:  # If outside board coords
            return False

        if old_pos == new_pos:  # Can't place on the same stack
            return False

        if len(self.board[old_pos]) ==  0:  # If the old stack is empty, invalid move
            return False
        
        if self.board[old_pos][-1][0] != self.next_turn:
            return False

        # Can't move from board to side-stacks
        if new_pos[0] == 0 or new_pos[0] == self.size + 1:
            return False

        if len(self.board[new_pos]) == 0:  # If the new stack is empty, can move
            return True

        # Neither of the two stacks are empty. Check the order.
        gobbler_piece = self.board[old_pos][-1]
        gobbled_piece = self.board[new_pos][-1]

        if gobbler_piece[1] > gobbled_piece[1]:
            return True

        return False

    def make_move(self, old_pos, new_pos):
        if self.can_move(old_pos, new_pos):
            top_piece = self.board[old_pos][-1]
            self.board[old_pos] = self.board[old_pos][:-1]
            self.board[new_pos].append(top_piece)

            self.next_turn = 'white' if self.next_turn == 'black' else 'black' # Update next palyer
            return True
        else:
            return False

    def enumerate_valid_moves(self, player):
        # Returns a list of valid move tuples of the form [(x, y)] for given player
        avail_moves = []

        for pos_x in self.board:
            if not self.board[pos_x]:
                continue

            curr_color = self.board[pos_x][-1][0]
            if curr_color != player:
                continue

            for pos_y in self.board:
                if self.can_move(pos_x, pos_y):
                    avail_moves.append((pos_x, pos_y))

        return avail_moves

    def print(self):
        for position, stack in self.board.items():
            print(f'{position}: {stack}')
            
            
    def check_win_loss(self, player_color):

        self.white_board = np.zeros([self.size, self.size])
        self.black_board = np.zeros([self.size, self.size])
        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                if len(self.board[(i, j)]) > 0:
                    top_piece = self.board[(i, j)][-1]
                    if top_piece[0] == 'white':
                        self.white_board[i-1, j-1] = 1
                    else:
                        self.black_board[i-1, j-1] = 1

        white_win = False
        black_win = False

        if np.any(np.sum(self.white_board, axis=0) == self.size) or \
            np.any(np.sum(self.white_board, axis=1) == self.size) or \
            sum(self.white_board[i, self.size-i-1] for i in range(self.size)) == self.size or \
            sum(self.white_board[i, i] for i in range(self.size)) == self.size:
                white_win = True

        if np.any(np.sum(self.black_board, axis=0) == self.size) or \
            np.any(np.sum(self.black_board, axis=1) == self.size) or \
            sum(self.black_board[i, self.size-i-1] for i in range(self.size)) == self.size or \
            sum(self.black_board[i, i] for i in range(self.size)) == self.size:
                black_win = True

        if white_win and black_win:
            return 'draw'
        elif white_win:
            return 'win' if player_color == 'white' else 'loss'
        elif black_win:
            return 'win' if player_color == 'black' else 'loss'
        else:
            return 'na'


if __name__ == '__main__':
    b = Board(4)
    r = Renderer(512)
    N = b.size + 1

    # print(b.next_turn)
    # Move from side-stack to board
    r.draw_board(b)
    # b.make_move((0, 1), (1, 1))
    # b.make_move((0, 3), (2, 3))
    b.make_move((0, 3), (2, 1))
    b.make_move((N, 3), (2, 1))
    r.draw_board(b)
    sleep(0.5)
    b.make_move((5, 3), (3, 4))
    r.draw_board(b)
    sleep(0.5)
    b.make_move((2, 3), (1, 1))
    r.draw_board(b)
    sleep(0.5)
    b.make_move((5, 2), (2, 3))
    # print(b.next_turn)
    # b.make_move((0, 4), (1, 1))
    r.draw_board(b)
    sleep(0.5)
    # b.make_move((N, 1), (2, 2))
    # r.draw_board(b)
    # sleep(0.5)
    # b.make_move((0, 1), (2, 3))
    # r.draw_board(b)

    # # Move from board space to board space
    # sleep(0.5)
    # b.make_move((2,  3), (4, 4)) # invalid
    # r.draw_board(b)

    # # Move from board space to side stack
    # b.make_move((4,  4), (0, 1))  # Invalid
    # r.draw_board(b)
    sleep(1)

    # enumerate possible_moves
    # white_moves = b.enumerate_valid_moves('white')
    # black_moves = b.enumerate_valid_moves('black')
    # print(white_moves)
    # print(black_moves)
