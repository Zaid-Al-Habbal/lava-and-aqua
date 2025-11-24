from copy import deepcopy as dc
from typing import Any
from core.action import MoveAction
from utils.types import GamePhase
from core.board import Board
from core.entitiy import Player
from core.engine import GameEngine

class GameState:
    
    def __init__(
        self,
        board: Board,
        phase: GamePhase = GamePhase.PLAYING,
        move_history: list[MoveAction] | None = None,
        move_count: int = 0,
    ):
        self.board = board
        self.phase = phase
        self.move_history = move_history if move_history is not None else []
        self.move_count = move_count

    @classmethod
    def from_level_data(cls, level_data: dict[str, Any]) -> "GameState":
        board = Board.from_dict(level_data)
        return cls(board=board, move_history=[])

    def get_player(self) -> Player | None:
        return self.board.get_player()

    def is_terminal(self) -> bool:
        return GameEngine.is_terminal(self.phase)

    def is_won(self) -> bool:
        return GameEngine.is_won(self.board, self.phase)

    def is_lost(self) -> bool:
        return GameEngine.is_lost(self.board, self.phase)

    def is_valid_action(self, action: MoveAction) -> bool:
        return GameEngine.is_valid_action(self.board, self.phase, action)

    def get_available_actions(self) -> list[MoveAction]:
        return GameEngine.get_available_actions(self.board, self.phase)

    def update_state(self, action: MoveAction) -> "GameState":

        player = self.board.get_player()

        self.board.apply_move(player, action.direction)

        self.board.spread_lava_and_water()
        self.board.tick_TIMED_DOORs()

        self.move_history.append(action)
        self.move_count += 1

        if GameEngine.is_won(self.board, self.phase):
            self.phase = GamePhase.WON
        elif GameEngine.is_lost(self.board, self.phase):
            self.phase = GamePhase.LOST
        
        return GameState(
            board=dc(self.board), phase=dc(self.phase), move_count=dc(self.move_count), move_history=dc(self.move_history)
        )

    def __str__(self) -> str:
        player = self.get_player()
        player_info = "No player"
        if player:
            player_info = f"Player at ({player.position.x}, {player.position.y})"
            orb_count = len(player.collected_orbs)
            if orb_count > 0:
                player_info += f" [Collected {orb_count} orbs]"

        return (
            f"GameState(Phase: {self.phase.value}, Moves: {self.move_count}, "
            f"{player_info})"
        )

    def __hash__(self) -> int:
        board_hash = hash(
            (
                self.board.width,
                self.board.height,
                tuple(sorted(self.board.entities.keys())),
                tuple(
                    (pos, tuple(sorted(ents)))
                    for pos, ents in sorted(self.board.position_map.items())
                ),
                self.board.player_id,
            )
        )
        return hash((board_hash, self.phase, self.move_count))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.__hash__() == other.__hash__()