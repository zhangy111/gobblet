#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:46:21 2021

@author: henry
"""
import pygame
from time import sleep


class Board:

    board = None
    free_pieces = None
    size = 0

    def __init__(self, board_size):
        '''
        Set up the board and initialize every space to None
        Pre-condition: board_size > 0
        Post-condition: board and free_pieces initialized
        '''

        rows = [i for i in range(1, board_size+1)]
        cols = [j for j in range(1, board_size+1)]  # could also use letters
        spaces = [(r, c) for r in rows for c in cols]
        self.board = dict(zip(spaces, [None for k in range(board_size ** 2)]))

        # also start tracking the 12 starting pieces for each player
        pieces = [(color, size) for color in ['black', 'white']
                  for size in [1, 2, 3, 4]]
        self.free_pieces = dict(zip(pieces, [3 for i in range(8)]))

        self.size = board_size

        print("Welcome to Gobblet.")

    def can_remove(self, test_piece, position):
        '''
        Check if the given piece can be removed from the given position
        Precondition: piece exists at position
        '''
        piece_stack = self.board[position]
        if piece_stack == None or len(piece_stack) == 0:
            print("Failed check. Empty position", position)
            return False

        for piece in piece_stack:
            if piece == test_piece:
                continue
            if piece[1] > test_piece[1]:
                print("Failed check. Cannot remove", test_piece,
                      "from", position, "due to presence of", piece)
                return False
        print("Passed check. Can remove", test_piece, "from", position)
        return True

    def remove_piece(self, test_piece, position):
        '''
        Updates board by removing a piece from the specified position
        Pre-condition: Can remove
        Post-condition: Removes piece from board
        '''
        piece_stack = self.board[position]
        piece_stack.remove(test_piece)
        if len(piece_stack) == 0:
            self.board[position] = None
        print("Updated piece stack at", position, ":", piece_stack)

    def place_piece(self, new_piece, position, old_position=None):
        '''
        Try to place a piece in the specified position. Return True for success
        else False.
        Pre-condition: 1) new_piece exists at old_position (if given)
                        2) position != old_position
        Post-condition: 1) new_piece is placed if successful or not placed if failed
                        2) new_piece is removed from existing location or the starting pile
        '''

        cur_piece_stack = self.board[position]
        print("Currently there is", cur_piece_stack, "at position", position)
        print("Trying to place", new_piece)

        # check validity of the request
        # case 1: no more requested piece available from the starting pile
        if old_position == None and self.free_pieces[new_piece] <= 0:
            print("Failed. There is no more free piece", new_piece)
            return False

        # case 2: request to move but the piece is being gobbled at old position
        if old_position != None:
            if self.can_remove(new_piece, old_position) == False:
                print("Failed. Cannot remove", new_piece,
                      "from old position", old_position)
                return False

        if cur_piece_stack != None:
            for cur_piece in cur_piece_stack:  # IM: Maybe just a check on the top most piece is enough?
                if cur_piece[1] >= new_piece[1]:
                    print("Failed.", new_piece, "cannot gobble", cur_piece)
                    return False
            cur_piece_stack.append(new_piece)
            print("Success. Updated stack at",
                  position, ":", self.board[position])
        else:
            new_piece_stack = [new_piece]
            self.board[position] = new_piece_stack
            print("Success. Updated stack at", position, ":", new_piece_stack)

        if old_position != None:
            self.remove_piece(new_piece, old_position)
        else:
            self.free_pieces[new_piece] -= 1

        return True

    def start_vis(self):  # setup pygame
        self.WIDTH = 512  # screen width
        pygame.init()
        pygame.display.set_caption("Gobblet!")
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.WIDTH))  # set canvas

    def update_vis(self):  # update board vis only when necessary
        pygame.display.flip()  # refresh buffer

        ROWS = self.size
        GRAY = (200, 200, 200)
        BLACK = (128, 51, 0)
        WHITE = (255, 194, 153)
        gap = self.WIDTH // ROWS

        # draw grid
        x = 0
        y = 0
        for i in range(ROWS):
            x = i * gap
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.WIDTH), 3)
            pygame.draw.line(self.screen, GRAY, (0, x), (self.WIDTH, x), 3)

        # add pieces
        for pos, stack in self.board.items():
            if stack is None:
                continue
            circle_center = tuple(gap * i - gap//2 for i in pos)
            for piece in stack:
                circle_color = WHITE if piece[0] == 'white' else BLACK
                radius = (piece[1] / self.size) * (gap // 3)
                pygame.draw.circle(self.screen, circle_color,
                                   circle_center, int(radius), 3)
        pygame.display.flip()

    def end_vis(self):  # housekeeping
        pygame.quit()


if __name__ == '__main__':
    b = Board(4)
    b.start_vis()
    b.place_piece(('black', 2), (1, 1))
    b.place_piece(('white', 3), (1, 1))  # should fail
    # I am not sure why this would fail? Is the piece ordering 1 > 2 > 3 > 4?
    # In that case should this be the other way around?
    # if cur_piece[1] >= new_piece[1]:
    # In the place_piece function
    b.update_vis()
    sleep(0.5)
    b.update_vis()
    sleep(0.5)
    b.end_vis()
