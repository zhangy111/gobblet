import copy
from score_jennifer import *
from board import Board

class SearchStrategy:

    def __init__(self, scoring_strategy, player_color, L):
        self.get_score = scoring_strategy
        self.player_color = player_color
        self.opp_color = 'white' if player_color == 'black' else 'black'

    def find_best_move(self, board, search_depth=2, normalized_strat=False):
        board = copy.deepcopy(board)
        best_move, minimax_val = self._minimax(board, search_depth, self.player_color) 
        # best_move, minimax_val = self._alphabeta(board, search_depth, -1e6, 1e6, self.player_color) 
        return best_move

    def _minimax(self, board, search_depth, curr_player):
        avail_moves = board.enumerate_valid_moves(curr_player)
        if search_depth == 0:
            return (avail_moves[0], self.get_score(board, self.player_color, board.size)) # Change board.size to L

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
    S = SearchStrategy(random_score, 'white', 4)
    b = Board(4)
    print(S.find_best_move(b))
