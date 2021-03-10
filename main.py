from score_henry import *
from score_jennifer import *
from search import *
from tournament import Tournament
from init import get_initial_board_states

if __name__ == '__main__':

    scoring_strats = get_all_scoring_functions()
    search_strats = ['montecarlo']
    
    all_game_strategies = []
    for search in search_strats:
        for score in scoring_strats:
            g = GameStrategy(score, search_depth=1, strategy_type=search)
            all_game_strategies.append(g)

    initial_states = get_initial_board_states()

    tournament = Tournament(all_game_strategies, initial_states, render=True)
    best_strategy = tournament.runRoundRobin()

    print(f'Best strategy index: {best_strategy}')
    all_game_strategies[best_strategy].pretty_print()
