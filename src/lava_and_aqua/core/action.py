from dataclasses import dataclass
from utils.types import Direction

@dataclass(frozen=True)
class MoveAction:
    direction: Direction

    def __init__(self, direction: Direction) -> None:
        object.__setattr__(self, 'direction', direction)

    def __str__(self) -> str:
        return f"MOVE {self.direction.name}"
