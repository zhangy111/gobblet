#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 17:16:36 2021

@author: henry
"""

from board import Board
from score_jennifer import ScoringStrategy
from score_jennifer import random_score
from score_jennifer import linarow_score
from score_jennifer import consecutive_score
from score_jennifer import freetomove_score
from renderer import Renderer


@ScoringStrategy
def get_all_scoring_functions():
    return

# @ScoringStrategy
def chess_like_score(board, player_color, piece_value=None, *args, **kwargs):
    """
    :param player_color: "white" or "black"
    :param board: Board object
    :param piece_value: Mapping of gobblets to value based on their sizes
    :return: score (net)
    """
    I_m = board.board
    score = 0
    
    if piece_value is None: # default value mapping
        piece_value = {('white', 1): 1, ('white', 2): 3, ('white', 3): 5, 
                       ('white', 4): 10, ('black', 1): 1, ('black', 2): 3,
                       ('black', 3): 5, ('black', 4): 10}
    
    for j in range (1, board.size+1):
        for k in range (1, board.size+1):
            if I_m.get((j, k)) is not None:
                pieces = I_m.get((j, k))
                #print(pieces)
                for piece in pieces:
                    if piece[0] == player_color:
                        score += piece_value[piece]
                    else:
                        score -= piece_value[piece]
    return score

def value_map_score(board, player_color, piece_value=None, diag_weight=1, 
                    *args, **kwargs):
    """
    :param player_color: "white" or "black"
    :param board: Board object
    :param piece_value: Mapping of gobblets to value based on their sizes
    :param diag_weight: Additional scoring weight applied to diagonal spaces
    :return: score (net)
    """
    I_m = board.board
    score = 0
    
    # diag_spaces = set() 
    # for i in range (1, board.size+1):
    #     diag_spaces.add((i, i))
    #     diag_spaces.add((i, board.size+1-i))
    # print(diag_spaces)
    
    if piece_value is None: # default value mapping
        piece_value = {('white', 1): 1, ('white', 2): 2, ('white', 3): 3, 
                       ('white', 4): 4, ('black', 1): 1, ('black', 2): 2,
                       ('black', 3): 3, ('black', 4): 4}
    
    for j in range (1, board.size+1):
        for k in range (1, board.size+1):    
            
            is_diag = 0
            if j == k or k == board.size + 1 - j:
                is_diag = 1
                
            if len(I_m.get((j, k))) > 0:
                pieces = I_m.get((j, k))
                #print(pieces)
                
                for piece in pieces:
                    if piece[0] == player_color:
                        score += piece_value[piece] * (1 + is_diag * diag_weight)
                    else:
                        score -= piece_value[piece] * (1 + is_diag * diag_weight)
                        
    return score


# @ScoringStrategy
def combo_score(board, player_color, L=4, piece_value=None, diag_weight=1, 
                    score_weight=None, *args, **kwargs):
    """
    :param player_color: "white" or "black"
    :param board: Board object
    :param L: L-in-a-row (must be less than board size)
    :param piece_value: Mapping of gobblets to value based on their sizes
    :param diag_weight: Additional scoring weight applied to diagonal spaces
    :return: score
    """
    score = 0
    
    if score_weight is None:
        score_weight = {'random': 1, 'linarow': 1, 'consecutive': 1, 
                         'freetomove': 1, 'chesslike': 1, 'valuemap': 1}

    score += random_score(board) * score_weight['random']
    score += linarow_score(board, player_color, L) * score_weight['linarow']
    score += consecutive_score(board, player_color, L) * score_weight['consecutive']
    # score += freetomove_score(board, player_color) * score_weight['freetomove']
    score += chess_like_score(board, player_color) * score_weight['chesslike']
    score += value_map_score(board, player_color) * score_weight['valuemap']
    
    return score


if __name__ == "__main__":
    # testing positive diagonal
    b = Board(4)
    N = b.size + 1
    b.make_move((0,1), (1,1))
    b.make_move((N,1), (1,2))
    b.make_move((0,1), (2,2))
    b.make_move((N,1), (2,4))
    b.make_move((0,1), (3,3))
    b.make_move((N,1), (3,4))
    b.make_move((0,1), (4,4))

    print(get_all_scoring_functions())

    # assert(value_map_score(b, 'white') == 11)
    # assert(value_map_score(b, 'black') == -11)
    # # testing negative diagonal
    # b.make_move((N,1), (3,2))
    # assert(value_map_score(b, 'white') == 9)
    # assert(value_map_score(b, 'black') == -9)
    # assert(chess_like_score(b, 'white') == 0)
    # assert(chess_like_score(b, 'black') == 0)
    # # testing moving (white, 4) from a diagonal into a nondiagonal
    # b.make_move((1,1), (1,3))
    # assert(value_map_score(b, 'white') == 5)
    # assert(chess_like_score(b, 'white') == 0)
    # # testing 2-piece stack
    # b.make_move((1,2), (2,2))
    # assert(value_map_score(b, 'white') == 1)
    # assert(chess_like_score(b, 'white') == 0)
    # # R = Renderer(512)
    # # R.draw_board(b)
