from typing import TypeAlias, NewType
from enum import Enum

# Basic types
Coordinate: TypeAlias = tuple[int, int]
EntityId = NewType("EntityId", int)


class Direction(Enum):
    """Cardinal directions for movement."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    @classmethod
    def from_key(cls, key: str) -> "Direction | None":
        """Convert keyboard input to direction."""
        mapping = {
            "w": cls.UP,
            "s": cls.DOWN,
            "a": cls.LEFT,
            "d": cls.RIGHT,
            "up": cls.UP,
            "down": cls.DOWN,
            "left": cls.LEFT,
            "right": cls.RIGHT,
        }
        return mapping.get(key.lower())


class EntityType(Enum):
    """Types of entities in the game."""
    PLAYER = "Player"
    LAVA = "Lava"
    WATER = "Water"
    METAL_BOX = "MetalBox"
    TIMED_DOOR = "TimedDoor"  
    CRACKED_WALL = "CrackedWall"
    PORTAL_ORB = "Orb"
    WALL = "Wall"
    GOAL = "Goal"  
    EMPTY = "Empty"  
    
class GamePhase(Enum):
    """Game state phases."""

    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
