from board import Board
from board_evaluator import BoardEvaluator
from piece import Piece

from dataclasses import dataclass


PIECE_VALUES: dict[Piece.Type, float] = {
    Piece.Type.PAWN: 1,
    Piece.Type.BISHOP: 3,
    Piece.Type.KNIGHT: 3,
    Piece.Type.ROOK: 5,
    Piece.Type.QUEEN: 15,
    Piece.Type.KING: 0,
}

CHECK_VALUE = 0
CHECKMATE_VALUE = 10000


@dataclass(frozen=True)
class PieceValueBoardEvalutor(BoardEvaluator):
    def _color_sign(self, piece_color: Piece.Color) -> float:
        return -1 if self.eval_color != piece_color else 1

    def evaluate(self, board: Board) -> float:
        value = 0
        for color in Piece.Color:
            if board.is_color_in_checkmate(color):
                return CHECKMATE_VALUE * self._color_sign(color.opponent)
            if board.is_color_in_check(color):
                value += CHECK_VALUE * \
                    self._color_sign(color.opponent)
        for piece in board.pieces:
            value += PIECE_VALUES[piece.type] * \
                self._color_sign(piece.color)
        return value
