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

    def print_search_details(self, algorithm_name):
        if self.solution is not None:
            duration = self.end_time - self.start_time
            for state in self.solution.path_states():
                print()
                print_board(state)
            print(f"{algorithm_name} Statistics:\n")
            print(f"Duration: {duration} seconds")
            print(f"Number of visited nodes: {self.num_of_visited_nodes}")
            print(f"Num of moves: {self.solution.path_cost}")
        else:
            print("No solution found")

    def dfs(self, node, depth_limit=200):

        # print_board(node.state)
        
        if self.solution or node.path_cost > depth_limit or node.state.phase == GamePhase.LOST:
            return
               
        if node.state.phase == GamePhase.WON:
            self.solution = node
            return
    
        hashed_state = node.state.__hash__()
        if hashed_state in self.visited:
            return
        
        self.visited.add(hashed_state)
        self.num_of_visited_nodes += 1

        for child in node.expand(self.problem):
            self.dfs(child)
            if self.solution:
                break   
            del child
        
        return

    def dfs2(self, problem, limit=80):
        
        frontier = deque([Node(problem.initial)])
        
        while frontier:
            node = frontier.pop()
            if node.state.phase == GamePhase.WON:
                self.solution = node
                return
            if node.path_cost > limit or node.state.phase == GamePhase.LOST:
                continue

            hashed_state = node.state.__hash__()
            if hashed_state in self.visited:
                continue
            
            self.visited.add(hashed_state)
            self.num_of_visited_nodes += 1

            for child in node.expand(self.problem):
                frontier.append(child)

    def bfs(self, problem, limit=200):
        

        frontier = deque([Node(problem.initial)])
        
        while frontier:
            node = frontier.pop()
            print_board(node.state)
            if node.state.phase == GamePhase.WON:
                self.solution = node
                return
            if node.state.phase == GamePhase.LOST or node.path_cost > limit:
                continue

            hashed_state = node.state.__hash__()
            if hashed_state in self.visited:
                continue
            
            self.visited.add(hashed_state)
            self.num_of_visited_nodes += 1

            for child in node.expand(problem):
                frontier.appendleft(child)
        return 
        
