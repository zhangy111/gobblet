import pygame
import copy
from time import sleep
import random
from score_jennifer import *
from board import Board
from renderer import Renderer

class GameStrategy:

    def __init__(self, scoring_strategy, search_depth=2, strategy_type='minimax', L=4):
        self.get_score = scoring_strategy
        self.strategy_type = strategy_type
        self.search_depth = search_depth

    def pretty_print(self):
        print('Scoring strat', self.get_score.__name__)
        print('Search strat', self.strategy_type)

    def find_best_move(self, board, player_color, normalized_strat=False):
        self.player_color = player_color
        self.opp_color = 'white' if player_color == 'black' else 'black'
        board = copy.deepcopy(board)

        if self.strategy_type == 'minimax':
            best_move, best_val = self._minimax(board, self.search_depth, self.player_color) 
        elif self.strategy_type == 'montecarlo':
            best_move, best_val = self._monte_carlo_ts(board, self.player_color, 16) 
        # else:
            # best_move, best_val = self._alphabeta(board, search_depth, -1e6, 1e6, self.player_color) 
        return best_move

    def _monte_carlo_ts(self, board, curr_player, search_depth, n_games=15):
        avail_moves = board.enumerate_valid_moves(curr_player)

        # Prune similar moves
        side_stack_id = 0 if curr_player == 'white' else board.size + 1
        remove_ids = []
        if len(board.board[(side_stack_id, 2)]) == len(board.board[(side_stack_id, 1)]):
            remove_ids.append(2) 
        if len(board.board[(side_stack_id, 3)]) == len(board.board[(side_stack_id, 2)]) or\
                len(board.board[(side_stack_id, 3)]) == len(board.board[(side_stack_id, 1)]):
            remove_ids.append(3)
        
        best_score = -1e6
        best_move = None

        for move in avail_moves:
            old_pos = move[0]

            if old_pos[0] == side_stack_id and old_pos[1] in remove_ids:
                continue

            curr_move_score = 0
            next_board = copy.deepcopy(board)
            next_board.make_move(*move)

            for i in range(n_games):
                curr_move_score += self._play_till_winner(next_board, curr_player, search_depth)
            if curr_move_score > best_score:
                best_score = curr_move_score
                best_move = move

        return best_move, best_score

    def _play_till_winner(self, board, start_player, search_depth):
        n_moves = search_depth

        # since starting with next state
        curr_color = 'white' if start_player == 'black' else 'black'

        for i in range(n_moves):
            result = board.check_win_loss(start_player)
            if result == 'win':
                return 1
            elif result == 'loss':
                return -1
            elif result == 'draw':
                return 0

            avail_moves = board.enumerate_valid_moves(curr_color)
            rand_move = random.choice(avail_moves)
            board.make_move(*rand_move)
            curr_color = 'white' if curr_color == 'black' else 'black'

        opp_player = 'white' if start_player == 'black' else 'black'

        # If more than n_moves are played check the value of the state
        # Assigning less than 1 to reflect less confidence in heuristics
        if self.get_score(board, start_player) > self.get_score(board, opp_player):
            return 0.1
        else:
            return -0.1 


    def _minimax(self, board, search_depth, curr_player):
        avail_moves = board.enumerate_valid_moves(curr_player)
        if search_depth == 0:
            return (avail_moves[0], self.get_score(board, self.player_color)) # Change board.size to L

        if curr_player == self.player_color: # Maximizing player
            max_val = -1e6 
            best_move = None             
            
            for move in avail_moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(*move) # Should avoid this
                next_move, next_val = self._minimax(board_copy, search_depth - 1, self.opp_color)
                if next_val > max_val:
                    max_val = next_val
                    best_move = move

            return best_move, max_val

        else: # Minimizing player
            min_val = 1e6 
            best_move = None             
            
            for move in avail_moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(*move) # Should avoid this
                next_move, next_val = self._minimax(board_copy, search_depth - 1, self.player_color)
                if next_val < min_val:
                    min_val = next_val
                    best_move = move

            return best_move, min_val

    def _alphabeta(self, board, search_depth, alpha, beta, curr_player):
        avail_moves = board.enumerate_valid_moves(curr_player)
        if search_depth == 0:
            return (avail_moves[0], self.get_score(board, self.player_color, board.size)) # Change board.size to L

        if curr_player == self.player_color: # Maximizing player
            max_val = -1e6 
            best_move = None             
            
            for move in avail_moves:
                board = copy.deepcopy(board)
                board.make_move(*move) # Should avoid this
                move, val = self._alphabeta(board, search_depth - 1, alpha, beta, self.opp_color)
                if val > max_val:
                    max_val = val
                    best_move = move

                alpha = max(alpha, max_val)
                if alpha >= beta:
                    break

            return best_move, max_val

        else: # Minimizing player
            min_val = 1e6 
            best_move = None             
            
            for move in avail_moves:
                board = copy.deepcopy(board)
                board.make_move(*move) # Should avoid this
                move, val = self._alphabeta(board, search_depth - 1, alpha, beta, self.player_color)
                if val < min_val:
                    min_val = val
                    best_move = move

                beta = min(beta, min_val)
                if beta <= alpha:
                    break

            return best_move, min_val

if __name__ == '__main__':
    S = GameStrategy(random_score, 'white', 4)
    b = Board(4)
    print(S.find_best_move(b))
