from score_henry import *
from score_jennifer import *
from search import *
from tournament import Tournament
from init import get_initial_board_states

if __name__ == '__main__':

    scoring_strats = get_all_scoring_functions()
    search_strats = ['montecarlo', 'minimax']
    
    all_game_strategies = []
    for search in search_strats:
        for score in scoring_strats:
            if search == 'minimax':
                g = GameStrategy(score, search_depth=2, strategy_type=search)
            elif search == 'montecarlo':
                g = GameStrategy(score, search_depth=6, strategy_type=search)
            all_game_strategies.append(g)

    initial_states = get_initial_board_states()

    tournament = Tournament(all_game_strategies, initial_states, render=False)
    results, best_strategy = tournament.runRoundRobin()

    print(f'Best strategy index: {best_strategy}')
    all_game_strategies[best_strategy].pretty_print()
    print(results)
    print(all_game_strategies[0].total_time / all_game_strategies[0].total_moves)
