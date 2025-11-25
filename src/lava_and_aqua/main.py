from ai.node import Node
from ai.search import SearchAlgorithm
from ai.problem import LavaAndAquaProblem
from core.state import GameState
from utils.rendering import print_board
from utils.level_loader import LevelLoader
from play import interactive_demo
import time

if __name__ == "__main__":
    # Run the demos
    # interactive_demo()
    level_path = LevelLoader.choose_level()
    level_data = LevelLoader.load_level(level_path)
    initial_state = GameState.from_level_data(level_data)
    problem = LavaAndAquaProblem(initial_state)
    search = SearchAlgorithm(problem)
    start_time = time.perf_counter()
    search.dfs(node=Node(state=initial_state))
    end_time = time.perf_counter()
    duration = end_time - start_time
    if search.solution is not None:
        for state in search.solution.path_states():
            print()
            print_board(state)
        print(f"Duration: {duration} seconds")
        print(f"Number of visited nodes: {search.num_of_visited_nodes}")
    else:
        print("No solution found")