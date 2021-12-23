from board import Board
from board_evaluator import BoardEvaluator
from piece import Piece

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property


@dataclass
class BoardTree(ABC):
    board: Board = field()
    board_evaluator: BoardEvaluator
    color: Piece.Color
    depth: int = 0
    children: list['BoardTree'] = field(default_factory=list)

    def __repr__(self) -> str:
        return self._repr(0)

    def _repr(self, indent: int) -> str:
        return f'\n{"  "*indent}{self.depth} {self.color.value} {repr(self.board)} {self.board_value}/{self.result.value}{"".join([child._repr(indent+1) for child in self.children])}'

    def expand(self) -> None:
        if not self.can_expand():
            return
        if self.children:
            return
        self.children = [
            self.create_child(
                board,
                self.board_evaluator,
                self.color.opponent,
                self.depth + 1,
            )
            for board in self.board.moves_for_color(self.color)
        ]

    def can_expand(self) -> bool:
        # no checkmates and everybody has to have a piece to move
        return not any([self.board.is_color_in_checkmate(color) for color in Piece.Color]) and all(self.board.pieces_by_color.values())

    def expand_to_depth(self, depth: int) -> None:
        if depth > 0 and self.can_expand():
            self.expand()
            for child in self.children:
                child.expand_to_depth(depth-1)

    @cached_property
    def board_value(self) -> float:
        return self.board_evaluator.evaluate(self.board)

    @abstractmethod
    def create_child(self, board: Board,
                     board_evaluator: BoardEvaluator,
                     color: Piece.Color,
                     depth: int) -> 'BoardTree': ...

    @dataclass(frozen=True)
    class Result:
        boards: list[Board]
        value: float

        def with_parent_board(self, parent_board: Board) -> 'BoardTree.Result':
            return BoardTree.Result([parent_board]+self.boards, self.value)

    @property
    @abstractmethod
    def result(self) -> 'BoardTree.Result': ...
