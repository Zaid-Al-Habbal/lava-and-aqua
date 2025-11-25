from utils.types import Coordinate, EntityType, EntityId
from core.entitiy import (
    Position,
    GameEntity,
)


class Board:
    def __init__(
        self,
        width: int,
        height: int,
        entities: dict[EntityId, GameEntity] | None = None,
        position_map: dict[Coordinate, list[EntityId]] | None = None,
        player_id: EntityId | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entities = entities or {}
        self.player_id = player_id

        if position_map is not None:
            self.position_map = position_map
        else:
            new_position_map: dict[Coordinate, list[EntityId]] = {}
            for entity_id, entity in self.entities.items():
                coord = entity.position.to_tuple()
                new_position_map.setdefault(coord, []).append(entity_id)
            self.position_map = new_position_map

    def get_entities_at(self, position: Position) -> list[GameEntity] | None:
        entities_id = self.position_map.get(position.to_tuple())
        if entities_id is None:
            return []
        return [self.entities[eid] for eid in entities_id]


    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height
    
    def add_entity(self, entity: GameEntity) -> None:
        self.entities[entity.entity_id] = entity
        self.position_map.setdefault(entity.position.to_tuple(), []).append(
            entity.entity_id
        )
    def remove_entity(self, entity_id: EntityId) -> None:
        entity = self.entities[entity_id]
        self.entities.pop(entity_id)

        coord = entity.position.to_tuple()
        self.position_map[coord].remove(entity_id)

    def update_entity(self, entity: GameEntity) -> None:
        self.remove_entity(entity.entity_id)
        self.add_entity(entity)

    def get_entities_by_type(self, entity_type: EntityType) -> list[GameEntity]:
        return [e for e in self.entities.values() if e.entity_type == entity_type]
    
    