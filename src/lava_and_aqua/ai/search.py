from collections import deque
from ai.node import Node
from utils.types import GamePhase
from utils.rendering import print_board
from .problem import Problem


class SearchAlgorithm:
    def __init__(self, problem: Problem) -> None:
        self.problem = problem
        self.solution = None
        self.num_of_visited_nodes = 0
        self.visited = set()
        self.start_time = None
        self.end_time = None

    def print_search_details(self):
        if self.solution is not None:
            duration = self.end_time - self.start_time
            for state in self.solution.path_states():
                print()
                print_board(state)
            print(f"Duration: {duration} seconds")
            print(f"Number of visited nodes: {self.num_of_visited_nodes}")
        else:
            print("No solution found")

    def dfs(self, node, depth_limit=80):
        
        if self.solution or depth_limit <= 0 or node.state.phase == GamePhase.LOST:
            return
               
        if node.state.phase == GamePhase.WON:
            self.solution = node
            return
    
        hashed_state = node.state.__hash__()
        if hashed_state in self.visited:
            return
        
        self.visited.add(hashed_state)
        self.num_of_visited_nodes += 1
    
        depth_limit -= 1

        for child in node.expand(self.problem):
            self.dfs(child, depth_limit)
            if self.solution:
                break   # Stop searching if a solution is found

        return

    def dfs2(self, problem, limit=100):
        
        frontier = deque([Node(problem.initial)])
        
        while frontier:
            node = frontier.pop()
            if node.state.phase == GamePhase.WON:
                self.solution = node
                return
            if len(node) >= limit or node.state.phase == GamePhase.LOST:
                continue

            hashed_state = node.state.__hash__()
            if hashed_state in self.visited:
                continue
            
            self.visited.add(hashed_state)
            self.num_of_visited_nodes += 1

            for child in node.expand(self.problem):
                frontier.append(child)

                    
        
