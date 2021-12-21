from piece import Piece
from position import Position
from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class Board:
    pieces: Mapping[Position, Piece] = field(default_factory=dict)

    def remove(self, at: Position) -> 'Board':
        return Board({pos: piece for pos, piece in self.pieces.items() if pos != at})

    def add(self, piece: Piece) -> 'Board':
        pieces = {pos: piece for pos, piece in self.pieces.items()}
        pieces[piece.position] = piece
        return Board(pieces)
