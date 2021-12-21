from position import Position
from dataclasses import dataclass

@dataclass(frozen=True)
class Piece:
    position: Position
