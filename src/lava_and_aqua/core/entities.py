from dataclasses import dataclass, field
from utils.types import Coordinate, EntityType, EntityId


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def move(self, dx: int, dy: int) -> "Position":
        return Position(self.x + dx, self.y + dy)

    def to_tuple(self) -> Coordinate:
        return (self.x, self.y)

    @classmethod
    def from_tuple(cls, coord: Coordinate) -> "Position":
        return cls(coord[0], coord[1])


@dataclass(frozen=True)
class Entity:
    entity_id: EntityId
    entity_type: EntityType
    position: Position

    def move_to(self, new_position: Position) -> "Entity":
        return Entity(
            entity_id=self.entity_id,
            entity_type=self.entity_type,
            position=new_position,
        )


def create_entity_class(entity_type: EntityType, class_name: str):
    @dataclass(frozen=True)
    class SimpleEntity(Entity):
        def __init__(self, entity_id: EntityId, position: Position) -> None:
            object.__setattr__(self, "entity_id", entity_id)
            object.__setattr__(self, "entity_type", entity_type)
            object.__setattr__(self, "position", position)

        def move_to(self, new_position: Position) -> "SimpleEntity":
            return self.__class__(entity_id=self.entity_id, position=new_position)

    SimpleEntity.__name__ = class_name
    SimpleEntity.__qualname__ = class_name
    return SimpleEntity


MetalBox = create_entity_class(EntityType.METAL_BOX, "MetalBox")
Wall = create_entity_class(EntityType.WALL, "Wall")
Goal = create_entity_class(EntityType.GOAL, "Goal")
Lava = create_entity_class(EntityType.LAVA, "Lava")
Water = create_entity_class(EntityType.WATER, "Water")
Orb = create_entity_class(EntityType.PORTAL_ORB, "Orb")
CrackedWall = create_entity_class(EntityType.CRACKED_WALL, "CrackedWall")


@dataclass(frozen=True)
class Player(Entity):
    collected_orbs: frozenset[EntityId] = field(default_factory=frozenset)

    def __init__(
        self,
        entity_id: EntityId,
        position: Position,
        collected_orbs: frozenset[EntityId] = frozenset(),
    ) -> None:
        object.__setattr__(self, "entity_id", entity_id)
        object.__setattr__(self, "entity_type", EntityType.PLAYER)
        object.__setattr__(self, "position", position)
        object.__setattr__(self, "collected_orbs", collected_orbs)

    def move_to(self, new_position: Position) -> "Player":
        return Player(
            entity_id=self.entity_id,
            position=new_position,
            collected_orbs=self.collected_orbs,
        )

    def collect_orb(self, orb_id: EntityId) -> "Player":
        new_orbs = self.collected_orbs | {orb_id}
        return Player(
            entity_id=self.entity_id, position=self.position, collected_orbs=new_orbs
        )


@dataclass(frozen=True)
class TimedDoor(Entity):
    remaining_time: int = 0

    def __init__(
        self, entity_id: EntityId, position: Position, remaining_time: int = 0
    ) -> None:
        object.__setattr__(self, "entity_id", entity_id)
        object.__setattr__(self, "entity_type", EntityType.TIMED_DOOR)
        object.__setattr__(self, "position", position)
        object.__setattr__(self, "remaining_time", remaining_time)

    def tick(self) -> "TimedDoor | None":
        new_time = self.remaining_time - 1
        if new_time <= 0:
            return None

        return TimedDoor(
            entity_id=self.entity_id, position=self.position, remaining_time=new_time
        )


GameEntity = Player | MetalBox | Wall | Goal | Lava | Water | Orb | CrackedWall | TimedDoor
