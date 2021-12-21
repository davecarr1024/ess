from piece import Piece
from position import Position

from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property
from typing import Callable, FrozenSet


@dataclass(frozen=True)
class Board:
    pieces: FrozenSet[Piece]

    def __post_init__(self):
        if len(self.pieces) != len(self.pieces_by_position):
            raise ValueError(f'duplicate piece positions {repr(self)}')

    def __str__(self) -> str:
        s = '\n'
        for y in range(7, -1, -1):
            s += f' {y+1} |'
            for x in range(8):
                position = Position(x, y)
                piece = self.pieces_by_position.get(position, None)
                if piece is None:
                    s += '    |'
                else:
                    s += f' {piece.color.value}{piece.type.value} |'
            s += '\n'
        s += '   |' + \
            ''.join([f' {chr(ord("a")+x)}  |' for x in range(8)]) + '\n'
        return s

    def with_piece(self, piece: Piece) -> 'Board':
        return Board(frozenset({piece}.union(self.pieces)))

    def without_piece(self, piece: Piece) -> 'Board':
        return Board(self.pieces - {piece})

    def with_piece_moved(self, piece: Piece, to_position: Position) -> 'Board':
        board = self
        to_piece = board.pieces_by_position.get(to_position, None)
        if to_piece is not None:
            board = board.without_piece(to_piece)
        return board.without_piece(piece).with_piece(piece.with_position(to_position))

    @cached_property
    def pieces_by_position(self) -> Mapping['Position', Piece]:
        return {piece.position: piece for piece in self.pieces}

    @cached_property
    def pieces_by_color(self) -> Mapping['Piece.Color', FrozenSet[Piece]]:
        return {color: frozenset({piece for piece in self.pieces if piece.color == color}) for color in Piece.Color}

    def _moves_for_linear_piece(self, deltas: FrozenSet[Position.Delta]) -> Callable[[Piece], FrozenSet['Board']]:
        def closure(piece: Piece) -> FrozenSet[Board]:
            boards: set[Board] = set()
            for delta in deltas:
                to_position = piece.position
                while to_position.can_add(delta):
                    to_position = to_position + delta
                    to_piece = self.pieces_by_position.get(to_position, None)
                    if to_piece is None:
                        boards.add(
                            self.with_piece_moved(piece, to_position))
                    elif to_piece.color != piece.color:
                        boards.add(
                            self.with_piece_moved(piece, to_position))
                        break
                    else:
                        break
            return frozenset(boards)
        return closure

    def _moves_for_deltas(self, deltas: FrozenSet[Position.Delta]) -> Callable[[Piece], FrozenSet['Board']]:
        def closure(piece: Piece) -> FrozenSet[Board]:
            boards: set[Board] = set()
            for delta in deltas:
                if piece.position.can_add(delta):
                    to_position = piece.position + delta
                    to_piece = self.pieces_by_position.get(to_position, None)
                    if to_piece is None or to_piece.color != piece.color:
                        boards.add(
                            self.with_piece_moved(piece, to_position))
            return frozenset(boards)
        return closure

    def _moves_for_pawn(self, piece: Piece) -> FrozenSet['Board']:
        boards: set[Board] = set()
        dy = 1 if piece.color == piece.Color.WHITE else -1

        def _move_if_empty(boards: set[Board], board: Board, delta: Position.Delta) -> None:
            if piece.position.can_add(delta):
                to_position = piece.position + delta
                if to_position not in self.pieces_by_position:
                    boards.add(self.with_piece_moved(piece, to_position))

        _move_if_empty(boards, self, Position.Delta(0, dy))
        if not piece.has_moved:
            _move_if_empty(boards, self, Position.Delta(0, dy*2))

        def _capture(dx: int) -> None:
            capture_delta = Position.Delta(dx, dy)
            if piece.position.can_add(capture_delta):
                to_position = piece.position + capture_delta
                to_piece = self.pieces_by_position.get(to_position, None)
                if to_piece is not None and to_piece.color != piece.color:
                    boards.add(self.with_piece_moved(piece, to_position))
        _capture(-1)
        _capture(1)

        # TODO pawn exchange, passing

        return frozenset(boards)

    @property
    def _move_funcs(self) -> Mapping[Piece.Type, Callable[[Piece], FrozenSet['Board']]]:
        return {
            Piece.Type.PAWN: self._moves_for_pawn,
            Piece.Type.BISHOP:
                self._moves_for_linear_piece(
                    frozenset({
                        Position.Delta(1, 1),
                        Position.Delta(1, -1),
                        Position.Delta(-1, 1),
                        Position.Delta(-1, -1),
                    })
                ),
            Piece.Type.ROOK:
                self._moves_for_linear_piece(
                    frozenset({
                        Position.Delta(1, 0),
                        Position.Delta(-1, 0),
                        Position.Delta(0, 1),
                        Position.Delta(0, -1),
                    })
                ),
            Piece.Type.QUEEN:
                self._moves_for_linear_piece(
                    frozenset({
                        Position.Delta(1, 1),
                        Position.Delta(1, -1),
                        Position.Delta(-1, 1),
                        Position.Delta(-1, -1),
                        Position.Delta(1, 0),
                        Position.Delta(-1, 0),
                        Position.Delta(0, 1),
                        Position.Delta(0, -1),
                    })
                ),
            Piece.Type.KING:
                self._moves_for_deltas(
                    frozenset({
                        Position.Delta(1, 1),
                        Position.Delta(1, -1),
                        Position.Delta(-1, 1),
                        Position.Delta(-1, -1),
                        Position.Delta(1, 0),
                        Position.Delta(-1, 0),
                        Position.Delta(0, 1),
                        Position.Delta(0, -1),
                    })
                ),
                # TODO castling
            Piece.Type.KNIGHT:
                self._moves_for_deltas(
                    frozenset({
                        Position.Delta(2, -1),
                        Position.Delta(2, 1),
                        Position.Delta(-2, -1),
                        Position.Delta(-2, 1),
                        Position.Delta(1, 2),
                        Position.Delta(-1, 2),
                        Position.Delta(1, -2),
                        Position.Delta(-1, -2),
                    })
                ),
        }

    def moves_for_piece(self, piece: Piece) -> FrozenSet['Board']:
        return self._move_funcs[piece.type](piece)

    def _moves_for_color_ignoring_check(self, color: Piece.Color) -> FrozenSet['Board']:
        boards: set[Board] = set()
        return frozenset(boards.union(*[self.moves_for_piece(piece)
                                        for piece in self.pieces if piece.color == color]))

    def moves_for_color(self, color: Piece.Color) -> FrozenSet['Board']:
        return frozenset({board for board in self._moves_for_color_ignoring_check(color) if not board.is_color_in_check(color)})

    def is_piece_threatened(self, piece: Piece) -> bool:
        return any([piece not in board.pieces for board in self._moves_for_color_ignoring_check(piece.color.opponent)])

    def pieces_of_type_and_color(self, type: Piece.Type, color: Piece.Color) -> FrozenSet[Piece]:
        return frozenset({piece for piece in self.pieces if piece.type == type and piece.color == color})

    def is_color_in_check(self, color: Piece.Color) -> bool:
        return any([self.is_piece_threatened(king) for king in self.pieces_of_type_and_color(Piece.Type.KING, color)])

    def is_color_in_checkmate(self, color: Piece.Color) -> bool:
        return self.is_color_in_check(color) and all([board.is_color_in_check(color) for board in self._moves_for_color_ignoring_check(color)])
