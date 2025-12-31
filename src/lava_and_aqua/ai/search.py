from collections import deque
import csv
import os
from ai.node import Node
from ai.priority_queue import PriorityQueue
from utils.types import EntityType, GamePhase
from utils.rendering import print_board
from .problem import Problem


class SearchAlgorithm:
    def __init__(self, problem: Problem) -> None:
        self.problem: Problem = problem
        self.solution: Node = None
        self.num_of_created_nodes: int = 1
        self.visited: set = set()
        self.start_time: float = None
        self.end_time: float = None
        self.dis: dict = {}

    def print_search_details(self, algorithm_name: str) -> None:
        if self.solution is not None:
            duration: float = self.end_time - self.start_time
            for state in self.solution.path_states():
                print()
                print_board(state)
            print(f"{algorithm_name} Statistics:\n")
            print(f"Duration: {duration} seconds")
            print(f"Number of created nodes: {self.num_of_created_nodes}")
            print(f"Number of visited nodes: {len(self.visited)}")
            print(f"Num of moves: {self.solution.path_cost}")
        else:
            print("No solution found")

    def save_search_details_to_csv(self, algorithm_name: str, game_level: str) -> None:
        if self.solution is None:
            return

        duration = self.end_time - self.start_time
        csv_file_path = f"statistics/{algorithm_name}.csv"

        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(csv_file_path)

        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)

            # Write headers if file is new
            if not file_exists:
                writer.writerow(
                    [
                        "Duration",
                        "Number of created nodes",
                        "Number of visited nodes",
                        "number of moves",
                        "game_level",
                    ]
                )

            # Write the data
            writer.writerow(
                [
                    duration,
                    self.num_of_created_nodes,
                    self.num_of_visited_nodes,
                    self.solution.path_cost,
                    game_level,
                ]
            )

    def dfs(self, node: Node) -> None:
        if node.state.phase == GamePhase.WON:
            self.solution = node
            return

        if node.state.phase == GamePhase.LOST:
            return

        hashed_state = hash(node.state)
        if hashed_state in self.visited:
            return

        self.visited.add(hashed_state)
        self.num_of_created_nodes += len(node.expand(self.problem))

        for child in node.expand(self.problem):
            self.dfs(child)
            if self.solution:
                break
            del child

    def bfs(self, start_node: Node) -> None:
        frontier = deque([start_node])

        while frontier:
            node = frontier.pop()

            if node.state.phase == GamePhase.WON:
                self.solution = node
                return
            if node.state.phase == GamePhase.LOST:
                continue

            hashed_state = hash(node.state)
            if hashed_state in self.visited:
                continue

            self.visited.add(hashed_state)

            for child in node.expand(self.problem):
                frontier.appendleft(child)
                self.num_of_created_nodes += 1

        return

    def ucs(self, start_node: Node) -> None:
        frontier = PriorityQueue([])

        hashed_start_state = hash(start_node.state)
        frontier.add((start_node.ucs_cost(), hashed_start_state, start_node))

        self.dis[hashed_start_state] = start_node.ucs_cost()

        while frontier:
            cost, hashed_state, node = frontier.pop()

            if node.state.phase == GamePhase.LOST:
                continue

            if node.state.phase == GamePhase.WON:
                self.solution = node
                return

            self.num_of_created_nodes += 1

            for child in node.expand(self.problem):
                hashed_child_state = hash(child.state)

                child_cost = child.ucs_cost()

                if (
                    hashed_child_state not in self.dis.keys()
                    or self.dis[hashed_child_state] > cost + child_cost
                ):
                    self.dis[hashed_child_state] = cost + child_cost
                    frontier.add((cost + child_cost, hashed_child_state, child))

    def hill_climbing_backtrack(self, start_node: Node) -> None:
        hashed_start_state = hash(start_node.state)

        if start_node.state.phase == GamePhase.LOST:
            return

        if start_node.state.phase == GamePhase.WON:
            self.solution = start_node
            return

        self.visited.add(hashed_start_state)

        frontier = PriorityQueue([])

        goal_list = start_node.state.board.get_entities_by_type(EntityType.GOAL)
        if len(goal_list) <= 0:
            return

        for child in start_node.expand(self.problem):
            hashed_child_state = hash(child.state)
            if child.state.get_player() is None:
                continue
            self.dis[hashed_child_state] = child.distance_to_the_goal(
                goal_list[0].position.to_tuple()
            )
            frontier.add((self.dis[hashed_child_state], hashed_child_state, child))

        while frontier:
            cost, hashed_state, node = frontier.pop()

            self.num_of_created_nodes += 1
            if hashed_state not in self.visited:
                self.hill_climbing_backtrack(node)
                if self.solution is not None:
                    return

    def a_star(self, start_node: Node) -> None:
        frontier = PriorityQueue([])

        hashed_start_state = hash(start_node.state)
        frontier.add((0, hashed_start_state, start_node))

        self.dis[hashed_start_state] = 0

        goal_list = start_node.state.board.get_entities_by_type(EntityType.GOAL)
        if len(goal_list) <= 0:
            return

        while frontier:
            cost, hashed_state, node = frontier.pop()

            if node.state.phase == GamePhase.LOST:
                continue

            if node.state.phase == GamePhase.WON:
                self.solution = node
                return

            self.num_of_created_nodes += 1

            cost += 1

            for child in node.expand(self.problem):
                hashed_child_state = hash(child.state)

                if child.state.get_player() is None:
                    continue

                child_cost = child.distance_to_the_goal(
                    goal_list[0].position.to_tuple()
                )

                if (
                    hashed_child_state not in self.dis.keys()
                    or self.dis[hashed_child_state] > cost + child_cost
                ):
                    self.dis[hashed_child_state] = cost + child_cost
                    frontier.add((cost + child_cost, hashed_child_state, child))