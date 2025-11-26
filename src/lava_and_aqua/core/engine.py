from typing import Any
from core.board import Board
from core.action import MoveAction
from core.observer import Observer
from utils.constants import FLUID_ENTITIES
from utils.types import Coordinate, EntityId, EntityType, GamePhase, Direction
from core.entitiy import (
    CrackedWall,
    Lava,
    Orb,
    Player,
    Goal,
    TimedDoor,
    Wall,
    MetalBox,
    Position,
    GameEntity,
    Water,
)

class GameEngine:
    
    @staticmethod
    def is_won(board: Board, phase: GamePhase) -> bool:
        if phase == GamePhase.WON:
            return True

        player = GameEngine.get_player(board)
        if player is None:
            return False

        if Observer.has_collected_all_orbs(board, player):
            for ent in board.get_entities_at(player.position):
                if isinstance(ent, Goal):
                    return True

        return False

    @staticmethod
    def is_lost(board: Board, phase: GamePhase) -> bool:
        if phase == GamePhase.LOST:
            return True

        player = GameEngine.get_player(board)
    
        if player is None or Observer.player_is_on_lava(board, player):
            return True

        goal_ent = board.get_entities_by_type(EntityType.GOAL)
        if len(goal_ent) == 0:
            return True
        
        if EntityType.LAVA in list(
            ent.entity_type for ent in board.get_entities_at(goal_ent[0].position)
        ):
            return True

        for ent in board.get_entities_at(player.position):
            if isinstance(ent, Wall):
                return True

        return False

    @staticmethod
    def is_terminal(phase: GamePhase) -> bool:
        return phase in [GamePhase.WON, GamePhase.LOST]
    
    @staticmethod
    def is_valid_action(board: Board, phase: GamePhase, action: MoveAction) -> bool:
        if GameEngine.is_terminal(phase):
            return False

        return Observer.is_valid_action(board, action)

    @staticmethod
    def get_available_actions(board: Board, phase: GamePhase) -> list[MoveAction]:
        if GameEngine.is_terminal(phase):
            return []

        available_actions: list[MoveAction] = []
        for direction in Direction:
            move_action = MoveAction(direction)
            if GameEngine.is_valid_action(board, phase, move_action):
                available_actions.append(move_action)

        return available_actions
    
    @classmethod
    def create_board_from_dict(cls, data: dict[str, Any]) -> "Board":
        width = data.get("width", 20)
        height = data.get("height", 15)

        entities: dict[EntityId, GameEntity] = {}
        position_map: dict[Coordinate, list[EntityId]] = {}
        player_id: EntityId | None = None

        next_id = 0
        entity_data = data.get("entities", {})

        def add_entity(entity: GameEntity) -> None:
            nonlocal next_id
            coord = entity.position.to_tuple()
            position_map.setdefault(coord, []).append(entity.entity_id)
            entities[entity.entity_id] = entity

        def parse_position(data: dict[str, Any]) -> Position:
            pos = data.get("position", [0, 0])
            return Position(pos[0], pos[1])

        def parse_entities_list(
            data_list: list[dict[str, Any]], entity_class, extra_args: dict = None
        ) -> None:
            nonlocal next_id
            extra_args = extra_args or {}
            for entity_item_data in data_list:
                entity = entity_class(EntityId(next_id), parse_position(entity_item_data), **extra_args)
                add_entity(entity)
                next_id += 1

        for player_data in entity_data.get("players", []):
            entity = Player(EntityId(next_id), parse_position(player_data))
            player_id = EntityId(next_id)
            add_entity(entity)
            next_id += 1

        parse_entities_list(entity_data.get("metal_boxes", []), MetalBox)
        parse_entities_list(entity_data.get("walls", []), Wall)
        parse_entities_list(entity_data.get("goals", []), Goal)
        parse_entities_list(entity_data.get("lavas", []), Lava)
        parse_entities_list(entity_data.get("waters", []), Water)
        parse_entities_list(entity_data.get("portal_orbs", []), Orb)
        parse_entities_list(entity_data.get("cracked_walls", []), CrackedWall)

        for timed_door_data in entity_data.get("timed_doors", []):
            timer = timed_door_data.get("timer", 5)
            entity = TimedDoor(
                EntityId(next_id), parse_position(timed_door_data), timer
            )
            add_entity(entity)
            next_id += 1

        return Board(
            width=width,
            height=height,
            entities=entities,
            position_map=position_map,
            player_id=player_id,
        )


    @staticmethod
    def get_player(board: Board) -> Player | None:
        if board.player_id is None:
            return None
        entity = board.entities.get(board.player_id)
        if isinstance(entity, Player):
            return entity
        return None
    
    @staticmethod
    def tick_TIMED_DOORs(board: Board) -> None:
        from core.observer import Observer

        return Observer.tick_timed_doors(board)
    @staticmethod
    def spread_lava_and_water(board: Board) -> None:
        from core.observer import Observer

        return Observer.spread_lava_and_water(board)
    
    @staticmethod
    def apply_move(board: Board, player: Player, direction: Direction) -> None:
        target_pos = player.position.move(direction.dx, direction.dy)
        entities_at_target = board.get_entities_at(target_pos)

        if entities_at_target is None:
            pass  
        else:
            box = None
            orb = None
            for ent in entities_at_target:
                if isinstance(ent, MetalBox):
                    box = ent
                elif isinstance(ent, Orb):
                    orb = ent
            if box is not None:
                box_target = target_pos.move(direction.dx, direction.dy)
                entity_behind_box = board.get_entities_at(box_target)

                if entity_behind_box is not None:
                    for ent in entity_behind_box:
                        if ent.entity_type in FLUID_ENTITIES:
                            board.remove_entity(ent.entity_id)

                moved_box = box.move_to(box_target)
                board.update_entity(moved_box)

            if orb is not None:
                player = player.collect_orb(orb.entity_id)
                board.remove_entity(orb.entity_id)

        moved_player = player.move_to(target_pos)
        board.update_entity(moved_player)
