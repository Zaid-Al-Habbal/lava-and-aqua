from typing import Any
from core.action import MoveAction
from utils.types import GamePhase, EntityType
from core.board import Board
from core.engine import GameEngine

class GameState:
    
    def __init__(
        self,
        board: Board,
        phase: GamePhase = GamePhase.PLAYING,
        move_count: int = 0,
        player=None,
    ):
        self.board = board
        self.phase = phase
        self.move_count = move_count
        self._player_cache = player

    @classmethod
    def from_level_data(cls, level_data: dict[str, Any]) -> "GameState":
        board = GameEngine.create_board_from_dict(level_data)
        player = GameEngine.get_player(board)
        return cls(board=board, player=player)

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
        # Copy board BEFORE mutating to avoid modifying the original
        new_board = self.board.copy()
        new_phase = self.phase
        new_move_count = self.move_count + 1
        
        player = GameEngine.get_player(new_board)

        GameEngine.apply_move(new_board, player, action.direction)

        if GameEngine.is_won(new_board, new_phase):
            new_phase = GamePhase.WON
        
        
        GameEngine.spread_lava_and_water(new_board)
        GameEngine.tick_TIMED_DOORs(new_board)

        if new_phase is not GamePhase.WON and GameEngine.is_lost(new_board, new_phase):
            new_phase = GamePhase.LOST
        
        next_player = GameEngine.get_player(new_board)
        return GameState(
            board=new_board, phase=new_phase, move_count=new_move_count, player=next_player
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
        entity_data = []
        for eid, ent in sorted(self.board.entities.items()):  # Sort by ID for determinism
            data = (eid, ent.position.to_tuple(), ent.entity_type)
            # Add entity-specific attributes if they exist
            if hasattr(ent, 'collected_orbs'):
                data = (*data, tuple(sorted(ent.collected_orbs)))  # Sort for consistency
            elif hasattr(ent, 'remaining_time'):
                data = (*data, ent.remaining_time)
            entity_data.append(data)
        
        board_hash = hash((tuple(entity_data), self.board.player_id))
        return hash((board_hash, self.move_count))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.__hash__() == other.__hash__()

    def get_player(self):
        if self._player_cache is None:
            self._player_cache = GameEngine.get_player(self.board)
        return self._player_cache