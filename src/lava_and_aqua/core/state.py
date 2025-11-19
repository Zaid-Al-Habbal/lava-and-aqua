from dataclasses import dataclass
from typing import Any
from core.actions import MoveAction
from utils.types import GamePhase
from core.board import Board
from core.entities import Player
from core.engine import GameEngine
from core.evaluator import GameEvaluator


@dataclass(frozen=True)
class GameState:

    board: Board
    phase: GamePhase = GamePhase.PLAYING
    move_history: list[MoveAction] = None
    move_count: int = 0

    @classmethod
    def from_level_data(cls, level_data: dict[str, Any]) -> "GameState":
        board = Board.from_dict(level_data)
        return cls(board=board, move_history=[])

    def get_player(self) -> Player | None:
        return self.board.get_player()

    def is_terminal(self) -> bool:
        return GameEvaluator.is_terminal(self.phase)

    def is_won(self) -> bool:
        return GameEvaluator.is_won(self.board, self.phase)

    def is_lost(self) -> bool:
        return GameEvaluator.is_lost(self.board, self.phase)

    def is_valid_action(self, action: MoveAction) -> bool:
        return GameEngine.is_valid_action(self.board, self.phase, action)

    def get_available_actions(self) -> list[MoveAction]:
        return GameEngine.get_available_actions(self.board, self.phase)

    def update_state(self, action: MoveAction) -> "GameState":
        new_board, new_phase, new_move_count = GameEngine.apply_action(
            self.board, self.phase, self.move_count, action
        )
        new_move_history = list(self.move_history)
        new_move_history.append(action)
        return GameState(
            board=new_board, phase=new_phase, move_count=new_move_count, move_history=new_move_history
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
        return (
            self.board.width == other.board.width
            and self.board.height == other.board.height
            and self.board.entities == other.board.entities
            and self.board.position_map == other.board.position_map
            and self.board.player_id == other.board.player_id
            and self.phase == other.phase
            and self.move_count == other.move_count
        )
