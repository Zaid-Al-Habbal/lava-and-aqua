from collections import deque
from core.state import GameState
from core.action import MoveAction
from core.game_manager import GameManager
from utils.types import Direction
from utils.level_loader import LevelLoader
from utils.rendering import print_board
from pyfiglet import Figlet

import os


def choose_level() -> str:
    levels_dir = "levels"
    level_files = [f for f in os.listdir(levels_dir) if f.endswith(".json")]
    if not level_files:
        print("No level files found in levels/")
        return None
    print("Available levels:")
    for idx, fname in enumerate(level_files):
        print(f"  {idx + 1}. {fname}")
    while True:
        choice = input("Choose a level by number: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(level_files):
                return os.path.join(levels_dir, level_files[idx])
        print("Invalid choice. Try again.")


def interactive_demo() -> None:
    print("\n" + "=" * 100)
    fig = Figlet(font='standard')
    print(fig.renderText('Lava & Aqua'))
    print("=" * 100)
    print()
    level_path = choose_level()
    if not level_path:
        print("No level selected. Exiting.")
        return
    level_data = LevelLoader.load_level(level_path)
    initial_state = GameState.from_level_data(level_data)
    game_state = initial_state
    GameManager.add_state(initial_state)
    print(f"Loaded level: {level_path}")
    print("  w/a/s/d - Move up/left/down/right")
    print("  r - Reset level")
    print("  u - Undo last move")
    print("  q - Exit demo")
    print()
    while True:
        print()
        print_board(game_state)
        print()
        print("You Available actions:",
            ", ".join([action.direction.name for action in game_state.get_available_actions()]))    
        command = input("\nEnter command: ").strip().lower()
        if command == "q":
            break
        elif command == "r":
            game_state = GameState.from_level_data(level_data)
            GameManager.game_states = deque([game_state])
            print("\nLevel reset!")
            print()
            print_board(game_state)
            continue
        elif command == "u":
            
            if game_state.__eq__(initial_state) is False:
                GameManager.remove_last_state()
                game_state = GameManager.game_states[-1]
                print("\nUndid last move!")
                print()
                print_board(game_state)
            else:
                print("No previous state to revert to!")
            continue
        # Parse movement commands
        if command in ["w", "a", "s", "d"]:
            direction_map = {
                "w": Direction.UP,
                "a": Direction.LEFT,
                "s": Direction.DOWN,
                "d": Direction.RIGHT,
            }
            action = MoveAction(direction_map[command])
        else:
            print("Unknown command")
            continue
        # Apply action
        if game_state.is_valid_action(action):
            game_state = game_state.update_state(action)
            print()
            print_board(game_state)
            GameManager.add_state(game_state)
            if game_state.is_won():
                print(
                    "🎉 Congratulations! You collected all orbs and reached the goal! 🎉 \n"
                )
                print(f"Your movement history:\n {[a.direction.name for a in game_state.move_history]}")
                break
            elif game_state.is_lost():
                print("💀 Game Over! You touched lava!")
                break
        else:
            print("Invalid action!")
    print("\nGame Over!")


if __name__ == "__main__":
    # Run the demos
    interactive_demo()
