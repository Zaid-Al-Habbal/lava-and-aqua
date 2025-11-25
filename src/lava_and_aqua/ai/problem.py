from core.state import GameState


class Problem:

    def __init__(self, initial=None): 
        self.__dict__.update(initial=initial) 
        
    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_over(self, state):        return NotImplementedError
    # def h(self, node):               return 0
    
    
class LavaAndAquaProblem(Problem):
    def __init__(self, initial=None):
        super().__init__(initial=initial)

    def actions(self, state: GameState):
        return state.get_available_actions()
    
    def result(self, state, action):
        return state.update_state(action)
    
    def is_over(self, state: GameState):
        return state.is_terminal()