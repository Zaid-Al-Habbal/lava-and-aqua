import time

from ai.search import SearchAlgorithm
from ai.problem import LavaAndAquaProblem
from core.state import GameState
from utils.rendering import print_board
from utils.level_loader import LevelLoader
from play import interactive_demo
from ai.node import Node

from pyfiglet import Figlet


def game_start():
    print("\n" + "=" * 100)
    fig = Figlet(font="standard")
    print(fig.renderText("Lava & Aqua"))
    print("=" * 100)
    print()
    level_path = LevelLoader.choose_level()
    if not level_path:
        print("No level selected. Exiting.")
        return
    level_data = LevelLoader.load_level(level_path)
    return level_data, level_path


def main():
    level_data, level_path = game_start()
    initial_state = GameState.from_level_data(level_data)
    print_board(initial_state)
    while True:
        print(
            "Game Modes:\n 1. User Play\n 2. DFS Play\n 3. BFS Play\n 4. UCS Play\n 5. Hill climbing Backtrack Play\n 6. A* Play"
        )
        command = input("\nEnter command: ").strip().lower()
        if command == "1":
            interactive_demo(initial_state, level_data)
            break
        else:
            problem = LavaAndAquaProblem(initial_state)
            search = SearchAlgorithm(problem)
            search.start_time = time.perf_counter()
            algorithm_name = None
            if command == "2":
                search.dfs(Node(initial_state))
                algorithm_name = "DFS"
            elif command == "3":
                search.bfs(Node(initial_state))
                algorithm_name = "BFS"
            elif command == "4":
                search.ucs(Node(initial_state))
                algorithm_name = "UCS"
            elif command == "5":
                search.hill_climbing_backtrack(Node(initial_state))
                algorithm_name = "Hill Climbing Backtrack"
            elif command == "6":
                search.a_star(Node(initial_state))
                algorithm_name = "A*"
            else:
                print("invalid command")
                continue

            search.end_time = time.perf_counter()
            search.print_search_details(algorithm_name)
            # search.save_search_details_to_csv(algorithm_name, level_path[7:-5])
            break


if __name__ == "__main__":
    main()
