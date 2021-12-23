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

        def __repr__(self) -> str:
            return self.value

        @staticmethod
        def parse(s: str) -> 'Piece.Color':
            for c in Piece.Color:
                if c.value == s:
                    return c
            raise ValueError(s)

    class Type(Enum):
        PAWN = 'p'
        KNIGHT = 'n'
        BISHOP = 'b'
        ROOK = 'r'
        QUEEN = 'q'
        KING = 'k'

        def __repr__(self) -> str:
            return self.value

        @staticmethod
        def parse(s: str) -> 'Piece.Type':
            for t in Piece.Type:
                if t.value == s:
                    return t
            raise ValueError(s)

    color: Color
    type: Type
    position: Position
    has_moved: bool = False

    def __repr__(self) -> str:
        return f'{self.color.value}{self.type.value}{repr(self.position)}'

    def with_position(self, position: Position) -> 'Piece':
        return Piece(self.color, self.type, position, True)

    @staticmethod
    def parse(s: str, has_moved: bool = True) -> 'Piece':
        if len(s) != 4:
            raise ValueError(s)
        return Piece(Piece.Color.parse(s[0]), Piece.Type.parse(s[1]), Position.parse(s[2:]), has_moved)
