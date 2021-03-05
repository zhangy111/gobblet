#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 00:16:40 2021

@author: henry

"""
import Board

class Game:
    
    num_turns = 0
    max_turns = 0
    player1_is_ai = False
    player2_is_ai = False
    player1_color = "white"
    player2_color = "black"
    I_m = None
    
    def __init__(self, max_turns, p1_ai, p2_ai, board_size=4):
        '''
        Set up the game
        Pre-condition: max_turns >= 0, board_size >0
        Post-condition: attributes updated
        '''
        self.max_turns = max_turns
        self.player1_is_ai = p1_ai
        self.player2_is_ai = p2_ai
        self.I_m = Board(board_size)
        
        
    def check_win_loss(self, player_color):
        '''
        Game ending condition checks
        Pre-condition: game board I_m where each board space is sorted s.t. 
                        the 0th element of the stack is the largest of the stack
        Post-condition: returns game state
        '''
        # this function uses indexing starting at 1 due to notation decisions
        if self.num_turns == self.max_turns:
            return 'draw'
        
        isHoriz = [0, 0, 0, 0] # tracking counts for horizontal columns
        isDiag = [0, 0] # [positive slope diagonal, negative slope diagonal]
         
        for j in range (1, self.I_m.size + 1): # j = [a, b, c, d] as described in notation
             isVert = 0 # tracking number of pieces of a player's color in a vertical column
             
             for k in range (1, self.I_m.size + 1):
                 if self.I_m[(j,k)] == None:
                     continue
                 topPiece = self.I_m[(j,k)][0] # only the top (visible) piece at $I_m[j][k]$ matters 
                 if topPiece[0] == player_color:
                     isVert += 1
                     isHoriz[k] += 1
                 else:
                     isVert -= 1
                     isHoriz[k] -= 1
                     
                 if j == k: # check if we are in a negative slope diagonal space 
                    if topPiece[0] == player_color:
                         isDiag[1] += 1
                    else:
                         isDiag[1] -= 1
                 if j + k == 5: # check if we are in a positive slope diagonal space 
                    if topPiece[0] == player_color:
                         isDiag[2] += 1
                    else:
                         isDiag[2] -= 1
                         
             if isVert == 4: # player 4-in-a-row 
                 return 'win'
             if isVert == -4: # opponent 4-in-a-row
                 return 'loss'
             
        for p in isHoriz: # tally up score for horizontal rows 
            if isHoriz[p] == 4:
                 return 'win'
            if isHoriz[p] == -4:
                 return 'loss'

        for q in [1, 2]: # tally up score for diagonals
            if isDiag[q] == 2:
                 return 'win'
            if isDiag[q] == -2:
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
            old_position = (int(old_position_row), int(old_position_col))
            new_position_row = input("Where is this piece going? Enter the row: ")
            new_position_col = input("Where is this piece going? Enter the column: ")
            new_position = (int(new_position_row), int(new_position_col))
            print("You want to move", piece, old_position, new_position)
            if old_position != (0,0):
                self.I_m.place_piece(piece, new_position, old_position)
            else:
                self.I_m.place_piece(piece, new_position)
               
    
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