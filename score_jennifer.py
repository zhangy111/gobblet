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

@ScoringStrategy
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
def linarow_score(board, player_color, L, *args, **kwargs):
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
            if I_m.get((j, k)) is not None:
                pieces = I_m.get((j, k))
                pieces.sort(key=lambda x: x[1], reverse=True)
                topcolor, topsize = pieces[0]
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
#
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

def consecutive_score(board, player_color, L, *args, **kwargs):
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
                if I_m.get((j, k)) is not None:
                    pieces = I_m.get((j, k))
                    pieces.sort(key=lambda x: x[1], reverse=True)
                    topcolor, topsize = pieces[0]
                    if topcolor == player_color:
                        consecCt += 1
            if consecCt >= L:
                score += 100

    # check horizontal columns
    for k in range(1, board.size+1):
        for start in range(1, board.size + 3 - L):
            consecCt = 0
            for j in range(start, min(start + L, board.size+1)):
                if I_m.get((j, k)) is not None:
                    pieces = I_m.get((j, k))
                    pieces.sort(key=lambda x: x[1], reverse=True)
                    topcolor, topsize = pieces[0]
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
            if I_m.get((m, m)) is not None:
                pieces = I_m.get((m, m))
                pieces.sort(key=lambda x: x[1], reverse=True)
                topcolor, topsize = pieces[0]
                if topcolor == player_color:
                    diag1 += 1

            # check negative diagonal
            if I_m.get((m, board.size+1-m)) is not None:
                pieces = I_m.get((m, board.size+1-m))
                pieces.sort(key=lambda x: x[1], reverse=True)
                topcolor, topsize = pieces[0]
                if topcolor == player_color:
                    diag2 += 1

        if diag1 >= L:
            score += 100
        if diag2 >= L:
            score += 100
    return score

# # testing
# # testing vertical columns
# b = Board(4)
# b.place_piece(('black', 3), (1,1))
# b.place_piece(('black', 4), (1,2))
# b.place_piece(('black', 2), (1,3))
# b.place_piece(('white', 1), (1,4))
# b.place_piece(('black', 2), (1,4))
# assert(consecutive_score('black', b, 4) == 100)
# assert(consecutive_score('black', b, 3) == 200)
# assert(consecutive_score('black', b, 2) == 300)
#
# # # testing horizontal rows
# b = Board(4)
# b.place_piece(('black', 3), (1,1))
# b.place_piece(('black', 4), (2,1))
# b.place_piece(('black', 2), (3,1))
# b.place_piece(('white', 1), (4,1))
# b.place_piece(('black', 2), (4,1))
# assert(consecutive_score('black', b, 4) == 100)
# assert(consecutive_score('black', b, 3) == 200)
# assert(consecutive_score('black', b, 2) == 300)
#
# # # testing positive diagonal
# b = Board(4)
# b.place_piece(('black', 3), (1,1))
# b.place_piece(('black', 4), (2,2))
# b.place_piece(('black', 2), (3,3))
# b.place_piece(('white', 1), (4,4))
# b.place_piece(('black', 2), (4,4))
# assert(consecutive_score('black', b, 4) == 100)
# assert(consecutive_score('black', b, 3) == 200)
# assert(consecutive_score('black', b, 2) == 300)
#
# # # testing negative diagonal
# b = Board(4)
# b.place_piece(('black', 3), (1,4))
# b.place_piece(('black', 4), (2,3))
# b.place_piece(('black', 2), (3,2))
# b.place_piece(('white', 1), (4,1))
# b.place_piece(('black', 2), (4,1))
# assert(consecutive_score('black', b, 4) == 100)
# assert(consecutive_score('black', b, 3) == 200)
# assert(consecutive_score('black', b, 2) == 300)


#
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
    I_m = board.board
    score = 0
    if player_color == "black":
        not_player_color = "white"
    else:
        not_player_color = "black"

    pieces = []  # tuples of (size, number of that piece available) for the player_color
    for (color, size) in board.free_pieces.keys():
        if color == player_color:
            pieces.append((size, board.free_pieces[(color, size)]))
    total = 0
    for (size, num) in pieces:
        total += num
    if total >= 3:  # STACKS = 3
        score += 100 * min(total, 3)

    for (j, k) in I_m.keys():

        if I_m.get((j, k)) is not None:
            pieces = I_m.get((j, k))
            pieces.sort(key=lambda x: x[1], reverse=True)
            topcolor, topsize = pieces[0]

            if topcolor == player_color:
                board_new = board
                board_new.remove_piece((topcolor, topsize), (j, k))
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
