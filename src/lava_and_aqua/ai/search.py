from collections import deque
import csv
import os
from ai.node import Node
from utils.types import GamePhase
from utils.rendering import print_board
from .problem import Problem


class SearchAlgorithm:
    def __init__(self, problem: Problem) -> None:
        self.problem = problem
        self.solution = None
        self.num_of_visited_nodes = 0
        self.num_of_created_nodes = 1
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
            print(f"Number of created nodes: {self.num_of_created_nodes}")
            print(f"Number of visited nodes: {self.num_of_visited_nodes}")
            print(f"Num of moves: {self.solution.path_cost}")
        else:
            print("No solution found")

    def save_search_details_to_csv(self, algorithm_name, game_level):
        if self.solution is None:
            return
        
        duration = self.end_time - self.start_time
        csv_file_path = f"statistics/{algorithm_name}.csv"
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(csv_file_path)
        
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write headers if file is new
            if not file_exists:
                writer.writerow(['Duration', 'Number of created nodes', 'Number of visited nodes', 'number of moves', 'game_level'])
            
            # Write the data
            writer.writerow([duration, self.num_of_created_nodes, self.num_of_visited_nodes, self.solution.path_cost, game_level])

    def dfs_rec(self, node):
        if self.solution is not None or node.state.phase == GamePhase.LOST:
            return
        
        if node.state.phase == GamePhase.WON:
            self.solution = node
            return
        
        hashed_state = node.state.__hash__()
        if hashed_state in self.visited:
            return 
        self.visited.add(hashed_state)
        self.num_of_visited_nodes += 1
        self.num_of_created_nodes += len(node.expand(self.problem))

        for child in node.expand(self.problem):
            self.dfs_rec(child)
            if self.solution:
                break
            del child
    
    def dfs_iter(self, problem, limit=200):
        
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
                self.num_of_created_nodes += 1

    def bfs(self, problem):
        frontier = deque([Node(problem.initial)])
        
        while frontier:
            node = frontier.pop()
            # print_board(node.state)
            if node.state.phase == GamePhase.WON:
                self.solution = node
                return
            if node.state.phase == GamePhase.LOST:
                continue

            hashed_state = node.state.__hash__()
            if hashed_state in self.visited:
                continue
            
            self.visited.add(hashed_state)
            self.num_of_visited_nodes += 1

            for child in node.expand(problem):
                frontier.appendleft(child)
                self.num_of_created_nodes += 1

        return 
        
    
    
