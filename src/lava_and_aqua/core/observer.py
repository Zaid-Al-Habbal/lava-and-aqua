from core.board import Board
from core.entitiy import Entity, GameEntity, Player, Position
from core.action import MoveAction
from utils.types import EntityType, EntityId, Direction
from utils.constants import SOLID_OBSTACLES, BLOCKING_ENTITIES, PASSABLE_WITH_FLUID


class Observer:

    @staticmethod
    def can_move(board: Board, player: Player, direction: Direction) -> bool:
        target_pos = player.position.move(direction.dx, direction.dy)

        if not board.is_within_bounds(target_pos):
            return False

        entities = board.get_entities_at(target_pos)

        if not entities:
            return True

        for entity in entities:
            ent_type = getattr(entity, "entity_type", None)

            if ent_type in SOLID_OBSTACLES:
                return False

            if ent_type == EntityType.METAL_BOX:
                return Observer.can_push_box(board, entity, direction)

        return True

    @staticmethod
    def can_push_box(board: Board, box: GameEntity, direction: Direction) -> bool:
        target_pos = box.position.move(direction.dx, direction.dy)

        if not board.is_within_bounds(target_pos):
            return False

        entity_at_target = board.get_entities_at(target_pos)

        if entity_at_target is None:
            return True

        for ent in entity_at_target:
            if ent.entity_type in BLOCKING_ENTITIES:
                return False

        return True

    @staticmethod
    def is_valid_action(board: Board, action: MoveAction) -> bool:
        player = board.get_player()
        return Observer.can_move(board, player, action.direction)


    @staticmethod
    def tick_timed_doors(board: Board) -> None:
        doors = board.get_entities_by_type(EntityType.TIMED_DOOR)
        for entity in doors:
            updated_entity = entity.tick()
            if updated_entity is None:
                board.remove_entity(entity.entity_id)
            else:
                board.update_entity(updated_entity)
    
    @staticmethod
    def player_is_on_lava(board: Board, player: Player) -> bool:
        entities_at_player = board.get_entities_at(player.position)
        return entities_at_player is not None and EntityType.LAVA in list(
            ent.entity_type for ent in entities_at_player
        )

    @staticmethod
    def has_collected_all_orbs(board: Board, player: Player) -> bool:
        all_orbs = board.get_entities_by_type(EntityType.PORTAL_ORB)
        if player is None:
            return False
        total_orbs_count = len(all_orbs) + len(player.collected_orbs)
        return len(player.collected_orbs) == total_orbs_count and len(all_orbs) == 0

    @staticmethod
    def spread_lava_and_water(board: Board) -> None:
        board_state = board
        next_id = max(board_state.entities.keys(), default=EntityId(-1)) + 1

        next_id = Observer._spread_fluid(
            board_state, EntityType.WATER, EntityType.LAVA, next_id
        )

        next_id =Observer._spread_fluid(
            board_state, EntityType.LAVA, EntityType.WATER, next_id
        )

    @staticmethod
    def _spread_fluid(
        board: Board,
        fluid_type: EntityType,
        collision_fluid: EntityType,
        next_id: int,
    ) -> int:
        positions_to_make_walls: set[Position] = set()
        new_fluid_positions: set[Position] = set()

        fluid_entities = board.get_entities_by_type(fluid_type)

        for fluid in fluid_entities:
            for direction in Direction:
                new_pos = fluid.position.move(direction.dx, direction.dy)
                if not board.is_within_bounds(new_pos):
                    continue

                entities_at_new = board.get_entities_at(new_pos)
                if not entities_at_new:
                    new_fluid_positions.add(new_pos)
                    continue

                entity_types = [e.entity_type for e in entities_at_new]

                if fluid_type in entity_types:
                    continue

                for ent in entities_at_new:
                    if ent.entity_type == collision_fluid:
                        positions_to_make_walls.add(new_pos)
                        break
                    elif ent.entity_type in PASSABLE_WITH_FLUID:
                        new_fluid_positions.add(new_pos)

        for pos in new_fluid_positions:
            fluid_entity = Entity(EntityId(next_id), fluid_type, pos)
            next_id += 1
            board.add_entity(fluid_entity)

        for pos in positions_to_make_walls:
            existings = board.get_entities_at(pos)
            for existing in existings:
                if existing is not None:
                    board.remove_entity(existing.entity_id)

            wall = Entity(EntityId(next_id), EntityType.WALL, pos)
            next_id += 1
            board.add_entity(wall)

        return next_id
