from collections import deque
from copy import deepcopy

from core.engine import GameEngine


class Node:
    def __init__(self, state, parent=None, action=None):
        self.__dict__.update(state=state, parent=parent, action=action)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    
    
    def expand(self, problem):
        "Expand a node, generating the children nodes."
        s = self.state
        sons = deque()
        for action in problem.actions(s):
            s1 = problem.result(deepcopy(s), action)
            sons.append(Node(s1, self, action))
        return sons
            

    def path_actions(self):
        if self.parent is None:
            return []
        return self.parent.path_actions() + [self.action]

    def path_states(self):
        if self.parent is None:
            return []
        return self.parent.path_states() + [self.state]
    
    def is_cycle(self, k=30):
        "Does this player path form a cycle of length k or less?"
        def find_cycle(ancestor, k):
            return (ancestor is not None and k > 0 and k % 2 == 0 and
                    (GameEngine.get_player(ancestor.state.board).position == GameEngine.get_player(self.state.board).position or find_cycle(ancestor.parent, k - 1)))
        return find_cycle(self.parent, k)


    