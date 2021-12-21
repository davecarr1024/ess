from piece import Piece
from position import Position

from unittest import TestCase


class PieceColorTest(TestCase):
    def test_opponent(self):
        self.assertEqual(Piece.Color.WHITE.opponent, Piece.Color.BLACK)
        self.assertEqual(Piece.Color.BLACK.opponent, Piece.Color.WHITE)


class PieceTest(TestCase):
    def test_with_position(self):
        self.assertEqual(
            Piece(
                Piece.Color.WHITE,
                Piece.Type.PAWN,
                Position.parse('c2')
            ).with_position(Position.parse('c4')),
            Piece(
                Piece.Color.WHITE,
                Piece.Type.PAWN,
                Position.parse('c4'),
                has_moved=True
            )
        )
