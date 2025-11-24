from utils.types import EntityType


DEFAULT_BOARD_WIDTH = 20
DEFAULT_BOARD_HEIGHT = 15


BLOCKING_ENTITIES = {
    EntityType.WALL,
    EntityType.TIMED_DOOR,
    EntityType.CRACKED_WALL,
    EntityType.METAL_BOX,
}

SOLID_OBSTACLES = {
    EntityType.WALL,
    EntityType.TIMED_DOOR,
    EntityType.CRACKED_WALL,
}

FLUID_ENTITIES = {EntityType.LAVA, EntityType.WATER}

NOT_PASSABLE_WITH_FLUID = {
    EntityType.WALL,
    EntityType.TIMED_DOOR,
    EntityType.METAL_BOX,
}