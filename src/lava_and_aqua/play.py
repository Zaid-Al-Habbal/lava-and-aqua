from collections import deque
from copy import deepcopy
from core.state import GameState
from core.action import MoveAction
from core.game_manager import GameManager
from utils.types import Direction
from utils.rendering import print_board

def interactive_demo(initial_state, level_data) -> None:
    
    game_state = initial_state
    GameManager.add_state(initial_state)
    print("  w/a/s/d - Move up/left/down/right")
    print("  r - Reset level")
    print("  u - Undo last move")
    print("  q - Exit demo")
    print()
    while True:
        print()
        print()
        print("Available actions:",
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
            
            if len(GameManager.game_states) > 1:
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
            GameManager.add_state(deepcopy(game_state))
            if game_state.is_won():
                print(
                    "🎉 Congratulations! You collected all orbs and reached the goal! 🎉 \n"
                )
                break
            elif game_state.is_lost():
                print("💀 Game Over! You touched lava!")
                break
        else:
            print("Invalid action!")
    print("\nGame Over!")

