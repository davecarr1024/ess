from board import Board
from piece import Piece
import piece_value_board_evaluator
from piece_value_board_evaluator import PieceValueBoardEvalutor
from position import Position

from unittest import TestCase


class PieceValueBoardEvalutorTest(TestCase):
    @staticmethod
    def _piece(pos: str, type: Piece.Type = Piece.Type.PAWN, color: Piece.Color = Piece.Color.WHITE, has_moved: bool = False) -> Piece:
        return Piece(color, type, Position.parse(pos), has_moved)

    @staticmethod
    def _board(*pieces: Piece) -> Board:
        return Board(frozenset(pieces))

    def test_friendly_pawn(self):
        self.assertEqual(
            PieceValueBoardEvalutor(Piece.Color.WHITE).evaluate(
                self._board(self._piece("e2", Piece.Type.PAWN, Piece.Color.WHITE))),
            piece_value_board_evaluator.PIECE_VALUES[Piece.Type.PAWN]
        )

    def test_enemy_pawn(self):
        self.assertEqual(
            PieceValueBoardEvalutor(Piece.Color.WHITE).evaluate(
                self._board(self._piece("e2", Piece.Type.PAWN, Piece.Color.BLACK))),
            -piece_value_board_evaluator.PIECE_VALUES[Piece.Type.PAWN]
        )

    def test_friendly_mate(self):
        self.assertEqual(
            PieceValueBoardEvalutor(Piece.Color.WHITE).evaluate(
                self._board(
                    self._piece("e1", Piece.Type.KING, Piece.Color.BLACK),
                    self._piece("a1", Piece.Type.ROOK, Piece.Color.WHITE),
                    self._piece("b2", Piece.Type.ROOK, Piece.Color.WHITE),
                )
            ),
            piece_value_board_evaluator.CHECKMATE_VALUE
        )

    def test_unfriendly_mate(self):
        self.assertEqual(
            PieceValueBoardEvalutor(Piece.Color.WHITE).evaluate(
                self._board(
                    self._piece("e1", Piece.Type.KING, Piece.Color.WHITE),
                    self._piece("a1", Piece.Type.ROOK, Piece.Color.BLACK),
                    self._piece("b2", Piece.Type.ROOK, Piece.Color.BLACK),
                )
            ),
            -piece_value_board_evaluator.CHECKMATE_VALUE
        )
