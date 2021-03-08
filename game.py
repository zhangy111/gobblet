#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 00:16:40 2021

@author: henry

"""
from board import Board
from search import SearchStrategy

class Game:
    
    num_turns = 0
    max_turns = 0
    player1_is_ai = False
    player2_is_ai = False
    player1_color = "white"
    player2_color = "black"
    b = None
    
    def __init__(self, max_turns=50, p1_ai=True, p2_ai=True, board_size=4):
        '''
        Set up the game
        Pre-condition: max_turns >= 0, board_size >0
        Post-condition: attributes updated
        '''
        self.max_turns = max_turns
        self.player1_is_ai = p1_ai
        self.player2_is_ai = p2_ai
        self.b = Board(board_size)
        
        
    def check_win_loss(self, player_color):
        '''
        Game ending condition checks
        Pre-condition: game board b where each board space is sorted s.t. 
                        the last element of the stack is the largest of the stack
        Post-condition: returns game state
        '''
        # this function uses indexing starting at 1 due to notation decisions
        if self.num_turns == self.max_turns:
            return 'draw'
        
        I_m = self.b.board
        win_flag = False
        loss_flag = False
        is_horiz = [0, 0, 0, 0] # tracking counts for horizontal columns
        is_diag = [0, 0] # [positive slope diagonal, negative slope diagonal]
         
        for j in range (1, self.b.size + 1): # j = [a, b, c, d] as described in notation
             is_vert = 0 # tracking number of pieces of a player's color in a vertical column
             
             for k in range (1, self.b.size + 1):
                 if len(I_m[(j,k)]) == 0:
                     continue
                 top_piece = I_m[(j,k)][-1] # get the largest piece
                 if top_piece[0] == player_color:
                     is_vert += 1
                     is_horiz[k-1] += 1
                 else:
                     is_vert -= 1
                     is_horiz[k-1] -= 1
                     
                 if j == k: # check if we are in a negative slope diagonal space 
                    if top_piece[0] == player_color:
                         is_diag[0] += 1
                    else:
                         is_diag[0] -= 1
                 if j + k == 5: # check if we are in a positive slope diagonal space 
                    if top_piece[0] == player_color:
                         is_diag[1] += 1
                    else:
                         is_diag[1] -= 1
                         
             if is_vert == 4: # player 4-in-a-row 
                 win_flag = True
             if is_vert == -4: # opponent 4-in-a-row
                 loss_flag = True
             
        for p in is_horiz: # tally up score for horizontal rows 
            if is_horiz[p] == 4:
                 win_flag = True
            if is_horiz[p] == -4:
                 loss_flag = True

        for q in [0, 1]: # tally up score for diagonals
            if is_diag[q] == 4:
                 win_flag = True
            if is_diag[q] == -4:
                 loss_flag = True

        # case when the move resulted in both player and opponent 4-in-a-row
        if win_flag and loss_flag:
            return 'draw'
        
        if win_flag:
            return 'win'
        
        if loss_flag:
            return 'loss'
        
        return 'na'
    
    
    def make_move(self, player):
        '''
        Simulates a "turn" in a game
        Pre-condition: player == 1 or 2
        Post-condition: the player has executed their move
        '''
        piece = None
        old_position = None
        new_position = None
        
        if player == 1 and self.player1_is_ai:
            pass
            # TODO - get optimal move from search strategy
            # this entails data about the piece, old position, and new position
            # old position == None means it's from the starting stack
        elif player == 2 and self.player2_is_ai:
            pass
            # TODO - get optimal move from search strategy
            # this entails data about the piece, old position, and new position
            # old position == None means it's from the starting stack
        else:
            piece_size = input("Size of the piece you want to move (enter a number): ")
            if player == 1:
                piece = (self.player1_color, int(piece_size)) # make piece tuple
            else:
                piece = (self.player2_color, int(piece_size)) # make piece tuple
            print("Are you moving it from the starting stack? If so, enter 0 for the below.")
            old_position_row = input("Where is this piece from? Enter the row: ")
            old_position_col = input("Where is this piece from? Enter the column: ")
            old_pos = (int(old_position_row), int(old_position_col))
            new_position_row = input("Where is this piece going? Enter the row: ")
            new_position_col = input("Where is this piece going? Enter the column: ")
            new_pos = (int(new_position_row), int(new_position_col))
            print("You want to move", piece, old_position, new_position)
            self.b.make_move(old_pos, new_pos)
               
    
    def run_game (self):
        '''
        Runs the game turns until some condition is reached
        Pre-condition: none
        Post-condition: the appropriate end game is triggered
        '''
        while True:
            state = self.check_win_loss(self.player2_color)
            if state != 'na':
                return_val = self.end_game(self.player2_color, state)
                return return_val
            self.make_move(1) # player 1 makes move
            self.num_turns += 1
            state = self.check_win_loss(self.player1_color)
            if state != 'na':
                return_val = self.end_game(self.player1_color, state)
                return return_val 
            self.make_move(2) # player 2 makes move
            self.num_turns += 1
    
    
    def end_game (self, player_color, condition):
        '''
        Performs some logic whenever a game end state is reached
        Standalone function so run_game wouldn't be encumbered
        Pre-condition: condition in {'win', 'loss', 'draw'}
        Post-condition: the appropriate value is returned
        '''
        if condition == 'draw':
            return 0
        if condition == 'win':
            return 1
        if condition == 'loss':
            return -1
        return 0
    
    
# testing positive diagonal
g = Game()
b = g.b
N = b.size + 1
b.make_move((0,1), (1,1))
b.make_move((N,1), (1,4))
b.make_move((0,1), (2,2))
b.make_move((N,1), (2,3))
b.make_move((0,1), (3,3))
b.make_move((N,1), (3,2))
b.make_move((0,1), (4,4))
assert(g.check_win_loss('white') == 'win')
# testing negative diagonal
b.make_move((N,1), (4,1))
b.make_move((4,4), (4,3))
assert(g.check_win_loss('black') == 'win')
