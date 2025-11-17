from utils.types import EntityType


DEFAULT_BOARD_WIDTH = 20
DEFAULT_BOARD_HEIGHT = 15


# Portal orbs
MUST_COLLECT_ALL_ORBS = True  # Player must collect all portal orbs to win


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

PASSABLE_WITH_FLUID = {
    EntityType.PLAYER,
    EntityType.GOAL,
    EntityType.PORTAL_ORB,
    EntityType.CRACKED_WALL,
}