from position import Position

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Piece:
    class Color(Enum):
        WHITE = 'w'
        BLACK = 'b'

        @property
        def opponent(self) -> 'Piece.Color':
            if self == Piece.Color.WHITE:
                return Piece.Color.BLACK
            else:
                return Piece.Color.WHITE

    class Type(Enum):
        PAWN = 'p'
        KNIGHT = 'n'
        BISHOP = 'b'
        ROOK = 'r'
        QUEEN = 'q'
        KING = 'k'

    color: Color
    type: Type
    position: 'Position'
    has_moved: bool = False

    def with_position(self, position: 'Position') -> 'Piece':
        return Piece(self.color, self.type, position, True)
