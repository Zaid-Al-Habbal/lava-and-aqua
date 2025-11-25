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
    
    def copy(self) -> "Board":
        """Create a shallow copy of the board. Entities are immutable, so we can reuse them."""
        return Board(
            width=self.width,
            height=self.height,
            entities=self.entities.copy(),  # Shallow copy dict (entities are immutable)
            position_map={coord: ids.copy() for coord, ids in self.position_map.items()},  # Copy lists in position_map
            player_id=self.player_id,
        )
    
    def has_entity_of_type(self, entity_type: EntityType) -> bool:
        """Check if the board currently holds at least one entity of the given type."""
        return any(e.entity_type == entity_type for e in self.entities.values())

    def has_any_entity_of_types(self, entity_types: tuple[EntityType, ...]) -> bool:
        """Fast check for whether any of the requested entity types exist on the board."""
        if not entity_types:
            return False
        type_set = set(entity_types)
        return any(e.entity_type in type_set for e in self.entities.values())
     