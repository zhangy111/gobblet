#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 5 15:44:57 2021

note: all testing was before any stack constraints were in place,
thus all testing has been commented out for future compilation

@author: Jennifer

Todo:
1) Decorate all other strategies
2) Verify order of kwargs
3) Incorporate design changes from board.py

"""
from board import Board
import random as rand
from operator import add

class ScoringStrategy:
    all_strats = []
    def __init__(self, strat):
        self.scoring_strat = strat
        if self.scoring_strat.__name__ != 'get_all_scoring_functions':
            self.all_strats.append(strat)

    def __call__(self, *args, **kwargs):
        if self.scoring_strat.__name__ == 'get_all_scoring_functions':
            return self.all_strats
        return self.scoring_strat(*args, **kwargs)

# @ScoringStrategy
def random_score(board, *args, **kwargs):
    """
    :param board: Board Object
    :return: sum of random scores generated for every space on the board
    """
    I_m = board.board
    score = 0
    for space in I_m.keys():
        score += rand.randint(0, 100)
    return score

# @ScoringStrategy
def linarow_score(board, player_color, L=4, *args, **kwargs):
    """
    :param player_color: "white" or "black"
    :param board: Board object
    :param L: L-in-a-row (must be less than board size)
    :return: score
    """
    I_m = board.board
    score = 0

    isHoriz = [[0, 0] for i in range(board.size)]
    isDiag = [[0, 0],[0, 0]]
    for j in range(1, board.size+1):
        isVert = [0, 0]
        for k in range (1, board.size+1):
            # get top piece
            if len(I_m.get((j, k))) > 0:
                topcolor, topsize = I_m.get((j, k))[-1]
                assert(I_m == board.board)
                if topcolor == player_color:
                    isVert = list(map(add, [1, 0], isVert))
                    isHoriz[k-1] = list(map(add, [1, 0], isHoriz[k-1]))
                if topcolor != player_color:
                    isVert = list(map(add, [0, 1], isVert))
                    isHoriz[k-1] = list(map(add, [0, 1], isHoriz[k-1]))
                if j == k:
                    if I_m.get((j, k)) == player_color:
                        isDiag[0] = list(map(add, [1, 0], isDiag[0]))
                    else:
                        isDiag[0] = list(map(add, [0, 1], isDiag[0]))
                if j+k == board.size+1:
                    if I_m.get((j, k)) == player_color:
                        isDiag[1] = list(map(add, [1, 0], isDiag[1]))
                    else:
                        isDiag[1] = list(map(add, [0, 1], isDiag[1]))
        if isVert[0] >= L:
            score += 100
        if isVert[1] >= L:
            score -= 100
    for p in range(0, len(isHoriz)):
        if isHoriz[p][0] >= L:
            score += 100
        if isHoriz[p][1] >= L:
            score -= 100
    for q in range(0, len(isDiag)):
        if isDiag[q][1] >= L:
            score += 100
        if isDiag[q][0] >= L:
            score -= 100
    return score

# # testing
# # testing vertical columns
# b = Board(4)
# print(random_score(b))
# b.place_piece(('black', 3), (1,1))
# b.place_piece(('black', 4), (1,2))
# b.place_piece(('black', 2), (1,3))
# b.place_piece(('white', 1), (1,4))
# b.place_piece(('black', 2), (1,4))
# assert(linarow_score('black', b, 4) == 100)
# assert(linarow_score('black', b, 3) == 100)
# assert(linarow_score('black', b, 2) == 100)

# # testing horizontal rows
# b = Board(4)
# b.place_piece(('black', 3), (1,1))
# b.place_piece(('black', 4), (2,1))
# b.place_piece(('black', 2), (3,1))
# b.place_piece(('white', 1), (4,1))
# b.place_piece(('black', 2), (4,1))
# assert(linarow_score('black', b, 4) == 100)
# assert(linarow_score('black', b, 3) == 100)
# assert(linarow_score('black', b, 2) == 100)
#
# # testing positive diagonal
# b = Board(4)
# b.place_piece(('black', 3), (1,1))
# b.place_piece(('black', 4), (2,2))
# b.place_piece(('black', 2), (3,3))
# b.place_piece(('white', 1), (4,4))
# b.place_piece(('black', 2), (4,4))
# assert(linarow_score('black', b, 4) == 100)
# assert(linarow_score('black', b, 3) == 100)
# assert(linarow_score('black', b, 2) == 100)
#
# # testing negative diagonal
# b = Board(4)
# b.place_piece(('black', 3), (1,4))
# b.place_piece(('black', 4), (2,3))
# b.place_piece(('black', 2), (3,2))
# b.place_piece(('white', 1), (4,1))
# b.place_piece(('black', 2), (4,1))
# assert(linarow_score('black', b, 4) == 100)
# assert(linarow_score('black', b, 3) == 100)
# assert(linarow_score('black', b, 2) == 100)

def agg_linarow_score(board, player_color, L=4, *args, **kwargs):
    agg_score = 0
    for i in range(L + 1):
        agg_score += (i**2) * linarow_score(board, player_color, i)

    return agg_score

def consecutive_score(board, player_color, L=4, *args, **kwargs):
    """
    :param player_color: "white" or "black"
    :param board: Board object
    :param L: check for L consecutive outtermost player_color pieces
    :return: score
    """
    I_m = board.board
    score = 0

    # check vertical columns
    for j in range(1, board.size+1):
        for start in range(1, board.size + 3 - L):
            consecCt = 0
            for k in range(start, min(start + L, board.size+1)):
                if len(I_m.get((j, k))) > 0:
                    topcolor, topsize = I_m.get((j, k))[-1]
                    if topcolor == player_color:
                        consecCt += 1
            if consecCt >= L:
                score += 100

    # check horizontal columns
    for k in range(1, board.size+1):
        for start in range(1, board.size + 3 - L):
            consecCt = 0
            for j in range(start, min(start + L, board.size+1)):
                if len(I_m.get((j, k))) > 0:
                    topcolor, topsize = I_m.get((j, k))[-1]
                    if topcolor == player_color:
                        consecCt += 1
            if consecCt >= L:
                score += 100

    # check diagonals

    for start in range(1, board.size + 2 - L):
        diag1 = 0
        diag2 = 0
        # check positive diagonal
        for m in range(start, min(start + L, board.size+1)):
            if len(I_m.get((m, m))) > 0:
                topcolor, topsize = I_m.get((m, m))[-1]
                if topcolor == player_color:
                    diag1 += 1

            # check negative diagonal
            if len(I_m.get((m, board.size+1-m))) > 0:
                topcolor, topsize = I_m.get((m, board.size+1-m))[-1]
                if topcolor == player_color:
                    diag2 += 1

        if diag1 >= L:
            score += 100
        if diag2 >= L:
            score += 100
    return score

def agg_consec_score(board, player_color, *args, **kwargs):
    agg_score = 0
    for i in range(board.size + 1):
        agg_score += (i**2) * consecutive_score(board, player_color, i)
    return agg_score

@ScoringStrategy
def agg_linarowconsec_score(board, player_color, *args, **kwargs):
    return agg_consec_score(board, player_color) + agg_linarow_score(board, player_color)

def comb(board, player_color, *args, **kwargs):
    return agg_consec_score(board, player_color) + 2*agg_linarow_score(board, player_color)

# @ScoringStrategy
def combo2(board, player_color, *args, **kwargs):
    return chess_like_score(board, player_color) + value_map_score(board, player_color)

def remove_top_layer(I_m, board_size=4, *args, **kwargs):
    """
    Helper function to remove top layer of pieces from the board
    :param board:
    :return:
    """
    for j in range(1, board_size+1):
        for k in range(1, board_size+1):
            if len(I_m.get((j, k))) > 0:
                I_m[(j, k)].pop()
    return I_m

def num_pieces(board, *args, **kwargs):
    I_m = board.board
    pieces = 0
    for elt in I_m.values():
        pieces += len(elt)
    return pieces


def combo3(board, player_color, *args, **kwargs):
    """
    strategy calculates agg_consec and agg_linarow for all levels of the board
    :param board:
    :param player_color:
    :param args:
    :param kwargs:
    :return:
    """
    I_m = board.board
    agg_score = 0
    for i in range(board.size):
        agg_score += agg_consec_score(board, player_color) + agg_linarow_score(board, player_color)
        I_m = remove_top_layer(I_m, board_size = board.size)
    return agg_score

def isGameOver(board, *args, **kwargs):
    """
    Helper function for freetomove_score()
    :param board: Board object
    :return: black/white/tie depending on winner player-color, otherwise returns -1
    """
    black_win = consecutive_score("black", board, board.size)
    white_win = consecutive_score("white", board, board.size)
    if black_win >= 100 and white_win >= 100:
        return "tie"
    elif black_win >= 100 and white_win <= 100:
        return "black"
    elif black_win <= 100 and white_win >= 100:
        return "white"
    else:
        return -1

def freetomove_score(board, player_color, *args, **kwargs):
    """
    :param player_color: black/white
    :param board: Board object
    :return: score
    """
    score = 0
    moves = board.enumerate_valid_moves("player_color")
    for (old_pos, new_pos) in moves:
        board.make_move(old_pos, new_pos)
        result = isGameOver(board_new)
        if result == player_color or result == -1:
            score += 100
        elif result == not_player_color:
            score -= 100
        else: # tie
            score += 50
    return score

# testing
# b = Board(4)
# assert(freetomove_score('black', b) == 300)
# b.place_piece(('black', 4), (1,1))
# assert(freetomove_score('black', b) == 400)

def combo4(board, player_color, *args, **kwargs):
    aggscore = agg_linarowconsec_score(board, player_color)
    aggscore += freetomove_score(board, player_color)
    return aggscore

def combo5(board, player_color, *args, **kwargs):
    return combo4(board, player_color) + combo_score(board, player_color)

def combo6(board, player_color, *args, **kwargs):
    return combo2(board, player_color) + combo4(board, player_color) + combo_score(board, player_color)

def combo7(board, player_color, *args, **kwargs):
    agg_score = chess_like_score(board, player_color) * agg_linarowconsec_score(board, player_color)
    agg_score += value_map_score(board, player_color) * agg_linarowconsec_score(board, player_color)
    return agg_score

def combo8(board, player_color, *args, **kwargs):
    aggscore = freetomove_score(board, player_color) * agg_linarowconsec_score(board, player_color)
    return combo7(board, player_color) + aggscore

def combo9(board, player_color, *args, **kwargs):
    aggscore = freetomove_score(board, player_color) * value_map_score(board, player_color)
    return combo7(board, player_color) + aggscore

def combo10(board, player_color, *args, **kwargs):
    aggscore = freetomove_score(board, player_color) * chess_like_score(board, player_color)
    return combo7(board, player_color) + aggscore
