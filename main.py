# from score_henry import get_all_scoring_functions
from score_jennifer import get_all_scoring_functions
from search import *
from tournament import Tournament
from init import get_initial_board_states
import glob_vars
import numpy as np
import time

if __name__ == '__main__':

    scoring_strats = get_all_scoring_functions()
    # search_strats = ['montecarlo', 'minimax']
    search_strats = ['minimax']

    for s in scoring_strats:
        print(s.__name__)
    # exit()

    num_strats = 8
    scoring_strats = scoring_strats[:num_strats]
    
    all_game_strategies = []
    for search in search_strats:
        for score in scoring_strats:
            if search == 'minimax':
                g = GameStrategy(score, search_depth=2, strategy_type=search)
            elif search == 'montecarlo':
                g = GameStrategy(score, search_depth=6, strategy_type=search)
            all_game_strategies.append(g)

    initial_states = get_initial_board_states()

    st = time.process_time()
    tournament = Tournament(all_game_strategies, initial_states, render=False)
    results, best_strategy = tournament.runRoundRobin()
    print(f"Time: {time.process_time() - st}")

    counts = glob_vars.outDegCounts
    avgCounts = sum(counts)/len(counts)
    print(f'Average available moves: {avgCounts}')
    print(f'Max available moves: {max(counts)}')
    print(f'Min available moves: {min(counts)}')
    print(f'Std-dev available moves: {np.std(counts)}')
    

    print(f'Best strategy index: {best_strategy}')
    all_game_strategies[best_strategy].pretty_print()
    print(results)
    print(all_game_strategies[0].total_time / all_game_strategies[0].total_moves)
