from collections import deque

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
            # No need to deepcopy - update_state now handles copying internally
            s1 = problem.result(s, action)
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
    

    