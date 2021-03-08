from match import Match

class Tournament:
    strategies = None
    start_configs = None
    render = False

    def __init__(self, strategies, start_configs, render=False):
        self.strategies = strategies
        self.start_configs = start_configs
        self.render = render

    def runRoundRobin(self):
        '''
        Runs a round robin tournament between all the strategies, where each
         match uses the provided start configurations
        Returns the index of the strategy with the largest average outcome 
         (implemented as largest cumulative outcome, since they're identical in 
         this case)
        '''
        cumResults = [0 for _ in self.strategies]
        n = len(self.strategies)
        for i in range(n):
            for j in range(i+1, n):
                match = Match(self.strategies[i], self.strategies[j], self.start_configs, render=self.render)
                result = match.run()
                cumResults[i] += result
                # invert result for player 2
                cumResults[j] += -result
        return cumResults.index(max(cumResults))

    def runSingleElimation(self):
        pass

