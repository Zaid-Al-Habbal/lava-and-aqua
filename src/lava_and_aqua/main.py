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
    fig = Figlet(font='standard')
    print(fig.renderText('Lava & Aqua'))
    print("=" * 100)
    print()
    level_path = LevelLoader.choose_level()
    if not level_path:
        print("No level selected. Exiting.")
        return
    level_data = LevelLoader.load_level(level_path)
    return level_data


if __name__ == "__main__":
    level_data = game_start()
    initial_state = GameState.from_level_data(level_data)
    print_board(initial_state)
    while True:
        print("Game Modes:\n 1. User Play\n 2. DFS Play\n 3. DFS2 Play\n 4. BFS Play")
        command = input("\nEnter command: ").strip().lower()
        if command == "1":
            interactive_demo(initial_state, level_data)
            break
        else:
            problem = LavaAndAquaProblem(initial_state)
            search = SearchAlgorithm(problem)
            search.start_time = time.perf_counter()
            if command == "2":
                search.dfs(Node(initial_state))
            elif command == "3":
                search.dfs2(problem)
            elif command == "4":
                search.bfs(problem)
            else:
                print("invalid command")
                continue

            search.end_time = time.perf_counter()
            search.print_search_details() 
            break   


