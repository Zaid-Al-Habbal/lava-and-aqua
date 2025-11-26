import struct
from typing import Any
import xxhash
from core.action import MoveAction
from utils.types import GamePhase
from core.board import Board
from core.engine import GameEngine


class GameState:
    
    def __init__(
        self,
        board: Board,
        phase: GamePhase = GamePhase.PLAYING,
        move_count: int = 0,
        player=None,
        _cached_hash: int = None  # NEW: Cache hash value
    ):
        self.board = board
        self.phase = phase
        self.move_count = move_count
        self._player_cache = player
        self._cached_hash = _cached_hash  # Cache the hash

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
        new_board = self.board.copy()
        new_phase = self.phase
        new_move_count = self.move_count + 1
        
        player = GameEngine.get_player(new_board)
        GameEngine.apply_move(new_board, player, action.direction)

        if GameEngine.is_won(new_board, new_phase):
            new_phase = GamePhase.WON  
        
        GameEngine.spread_lava_and_water(new_board)
        GameEngine.tick_TIMED_DOORs(new_board)

        if GameEngine.is_lost(new_board, new_phase) and new_phase != GamePhase.WON:
            new_phase = GamePhase.LOST
        
        next_player = GameEngine.get_player(new_board)
        return GameState(
            board=new_board, 
            phase=new_phase, 
            move_count=new_move_count, 
            player=next_player,
            _cached_hash=None  # Will be computed on first __hash__() call
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
        if self._cached_hash is not None:
            return self._cached_hash

        hasher = xxhash.xxh64()

        position_to_entities: dict[tuple[int, int], list[tuple[str, Any]]] = {}
        
        for ent in self.board.entities.values():
            pos = (ent.position.x, ent.position.y)
            entity_type = ent.entity_type.value
            
            # Collect extra data for special entities
            extra_data = None
            if hasattr(ent, "collected_orbs"):
                extra_data = tuple(sorted(int(x) for x in ent.collected_orbs))
            elif hasattr(ent, "remaining_time"):
                extra_data = ent.remaining_time
            
            if pos not in position_to_entities:
                position_to_entities[pos] = []
            
            position_to_entities[pos].append((entity_type, extra_data))
        
        # Sort positions for deterministic hashing
        sorted_positions = sorted(position_to_entities.items())
        
        hasher.update(struct.pack("<i", len(sorted_positions)))
        
        for pos, entities_at_pos in sorted_positions:
            hasher.update(struct.pack("<ii", pos[0], pos[1]))
            
            entities_at_pos.sort()
            
            hasher.update(struct.pack("<i", len(entities_at_pos)))
            
            for entity_type, extra_data in entities_at_pos:
                hasher.update(entity_type.encode("utf-8"))
                
                if extra_data is not None:
                    if isinstance(extra_data, tuple):
                        hasher.update(struct.pack("<i", len(extra_data)))
                        for orb in extra_data:
                            hasher.update(struct.pack("<i", orb))
                    elif isinstance(extra_data, int):
                        hasher.update(struct.pack("<i", extra_data))

        self._cached_hash = hasher.intdigest()
        return self._cached_hash
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.__hash__() == other.__hash__()

    def get_player(self):
        if self._player_cache is None:
            self._player_cache = GameEngine.get_player(self.board)
        return self._player_cache