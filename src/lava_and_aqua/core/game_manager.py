from collections import deque

from core.state import GameState


class GameManager:
    game_states: deque[GameState] = deque()

    @staticmethod
    def add_state(state: GameState) -> None:
        GameManager.game_states.append(state)

    @staticmethod
    def remove_last_state() -> GameState | None:
        if GameManager.game_states:
            return GameManager.game_states.pop()
        return None
