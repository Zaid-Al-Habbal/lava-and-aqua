from dataclasses import dataclass, field
from typing import Any
from utils.constants import FLUID_ENTITIES
from utils.types import Coordinate, Direction, EntityType, EntityId
from core.entities import (
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


@dataclass(frozen=True)
class Board:
    width: int
    height: int
    entities: dict[EntityId, GameEntity] = field(default_factory=dict)
    position_map: dict[Coordinate, list[EntityId]] = field(default_factory=dict)
    player_id: EntityId | None = None

    def __post_init__(self) -> None:
        new_position_map: dict[Coordinate, list[EntityId]] = {}
        for entity_id, entity in self.entities.items():
            coord = entity.position.to_tuple()
            new_position_map.setdefault(coord, []).append(entity_id)

        object.__setattr__(self, "position_map", new_position_map)

    def _copy_position_map(self) -> dict[Coordinate, list[EntityId]]:
        return {k: list(v) for k, v in self.position_map.items()}

    def _create_board(
        self,
        entities: dict[EntityId, GameEntity],
        position_map: dict[Coordinate, list[EntityId]],
        player_id: EntityId | None = None,
    ) -> "Board":
        return Board(
            width=self.width,
            height=self.height,
            entities=entities,
            position_map=position_map,
            player_id=player_id or self.player_id,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Board":
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

        return cls(
            width=width,
            height=height,
            entities=entities,
            position_map=position_map,
            player_id=player_id,
        )

    def get_entities_at(self, position: Position) -> list[GameEntity] | None:
        entities_id = self.position_map.get(position.to_tuple())
        if entities_id is None:
            return []
        return [self.entities[eid] for eid in entities_id]


    def get_player(self) -> Player | None:
        if self.player_id is None:
            return None
        entity = self.entities.get(self.player_id)
        if isinstance(entity, Player):
            return entity
        return None


    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def update_entity(self, entity: GameEntity) -> "Board":
        new_entities = dict(self.entities)

        old_entity = new_entities.get(entity.entity_id)
        new_position_map = self._copy_position_map()

        if old_entity is not None:
            old_coord = old_entity.position.to_tuple()
            if old_coord in new_position_map:
                new_position_map[old_coord].remove(entity.entity_id)

        new_entities[entity.entity_id] = entity
        new_position_map.setdefault(entity.position.to_tuple(), []).append(
            entity.entity_id
        )

        return self._create_board(new_entities, new_position_map)

    def remove_entity(self, entity_id: EntityId) -> "Board":
        if entity_id not in self.entities:
            return self

        entity = self.entities[entity_id]
        new_entities = {eid: e for eid, e in self.entities.items() if eid != entity_id}
        new_position_map = self._copy_position_map()

        coord = entity.position.to_tuple()
        if coord in new_position_map:
            new_position_map[coord].remove(entity_id)

        return self._create_board(new_entities, new_position_map)

    def add_entity(self, entity: GameEntity) -> "Board":
        new_entities = dict(self.entities)
        new_position_map = self._copy_position_map()

        new_entities[entity.entity_id] = entity
        new_position_map.setdefault(entity.position.to_tuple(), []).append(
            entity.entity_id
        )

        return self._create_board(new_entities, new_position_map)

    def get_entities_by_type(self, entity_type: EntityType) -> list[GameEntity]:
        return [e for e in self.entities.values() if e.entity_type == entity_type]
    
    def apply_move(self, player: Player, direction: Direction) -> "Board":
        target_pos = player.position.move(direction.dx, direction.dy)
        entities_at_target = self.get_entities_at(target_pos)

        board = self

        if entities_at_target is None or len(entities_at_target) == 0:
            pass  
        else:
            box = None
            for entBox in entities_at_target:
                if isinstance(entBox, MetalBox):
                    box = entBox
                    break
            if box is not None:
                box_target = target_pos.move(direction.dx, direction.dy)
                entity_behind_box = board.get_entities_at(box_target)

                if entity_behind_box is not None:
                    for ent in entity_behind_box:
                        if ent.entity_type in FLUID_ENTITIES:
                            board = board.remove_entity(ent.entity_id)

                moved_box = entities_at_target[0].move_to(box_target)
                board = board.update_entity(moved_box)

            orb = None
            for entOrb in entities_at_target:
                if isinstance(entOrb, Orb):
                    orb = entOrb
                    break
            if orb is not None:
                player = player.collect_orb(orb.entity_id)
                board = board.remove_entity(orb.entity_id)

        moved_player = player.move_to(target_pos)
        board = board.update_entity(moved_player)

        return board

    def tick_TIMED_DOORs(self) -> "Board":
        from core.observers import Observer

        return Observer.tick_timed_doors(self)

    def spread_lava_and_water(self) -> "Board":
        from core.observers import Observer

        return Observer.spread_lava_and_water(self)
