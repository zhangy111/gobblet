from score_henry import *
from score_jennifer import *
from search import *

if __name__ == '__main__':

    scoring_strats = get_all_scoring_functions()
    search_strats = ['minimax']
    
    all_game_strategies = []
    for search in search_strats:
        for score in scoring_strats:
            g = GameStrategy(score, search_depth=2, strategy_type=search)
            all_game_strategies.append(g)

    print(all_game_strategies)
