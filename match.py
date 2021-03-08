from game import Game
import copy

class Match:
    
    p1_strategy = None
    p2_strategy = None
    start_configs = None
    render = False

    def __init__(self, p1_strategy, p2_strategy, start_configs, render=False):
        '''
        Set up a match between two strategies
        p1_strategy and p2_strategy are both instances of GameStrategy
        start_configs is a list of Boards
        '''
        self.p1_strategy = p1_strategy
        self.p2_strategy = p2_strategy
        self.start_configs = start_configs
        self.render = render

    def run(self):
        '''
        Run the match by playing a 2 games for every starting configuration, one
         where p1 is white and one where p2 is white
        Returns a fp value in [-1, 1], which is the average result of every game
         played
        '''
        cum_result = 0
        for start_config in self.start_configs:
            board1 = copy.deepcopy(start_config)
            game1 = Game(self.p1_strategy, self.p2_strategy, board=board1, render=self.render)
            result = game1.run_game()
            cum_result += result
            print()
            board2 = copy.deepcopy(start_config)
            board2.print()
            print(board2.enumerate_valid_moves('white'))
            game2 = Game(self.p2_strategy, self.p1_strategy, board=board2, render=self.render)
            result = game2.run_game()
            cum_result += result
        return cum_result / (2 * len(self.start_configs))


if __name__ == "__main__":
    from board import Board
    from init import BoardInitializer
    from search import GameStrategy
    from score_jennifer import random_score

    s1 = GameStrategy(random_score, 'white', 4)
    s2 = GameStrategy(random_score, 'black', 4)

    num_configs = 1
    start_configs = []
    I = BoardInitializer('random')
    for _ in range(num_configs):
        board = Board()
        I(board)
        start_configs.append(board)

    
    m = Match(s1, s2, start_configs)
    result = m.run()
    print(result)

        
