from collections import deque

from core.entitiy import Position
from utils.types import EntityType

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    
    
    def expand(self, problem):
        "Expand a node, generating the children nodes."
        s = self.state
        sons = deque()
        for action in problem.actions(s):
            # No need to deepcopy - update_state now handles copying internally
            s1 = problem.result(s, action)
            sons.append(Node(s1, self, action, self.path_cost + 1))
        return sons
            

    def path_actions(self):
        if self.parent is None:
            return []
        return self.parent.path_actions() + [self.action]

    def path_states(self):
        if self.parent is None:
            return []
        return self.parent.path_states() + [self.state]
    

    def ucs_cost(self):
        return len(self.state.board.get_entities_by_type(EntityType.LAVA))
    

    # goal_list = node.state.board.get_entities_by_type(EntityType.GOAL)
    #         if len(goal_list) > 0:
    #             print(f"distance to goal: {node.distance_to_the_goal(goal_list[0].position)}")
    def distance_to_the_goal(self, goal_pos : tuple[int, int]) -> int:
        player_pos = self.state.get_player().position.to_tuple()
        px, py = player_pos
        gx, gy = goal_pos
        return abs(px - gx) + abs(py - gy)