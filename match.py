from game import Game

class Match:
    
    p1_strategy = None
    p2_strategy = None
    start_configs = None

    def __init__(self, p1_strategy, p2_strategy, start_configs):
        '''
        Set up a match between two strategies
        p1_strategy and p2_strategy are both instances of SearchStrategy
        start_configs is a list of Boards
        '''
        self.p1_strategy = p1_strategy
        self.p2_strategy = p2_strategy
        self.start_configs = start_configs

    def run(self):
        '''
        Run the match by playing a game for every starting configuration
        Returns a fp value in [-1, 1], which is the average result of every game
         played
        '''
        cum_result = 0
        for start_config in self.start_configs:
            game = Game(self.p1_strategy, self.p2_strategy, board=start_config)
            result = game.run_game()
            cumResult += result
        return cum_result / len(self.start_configs)
        
