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

    def test_parse_color(self):
        self.assertEqual(Piece.Color.WHITE, Piece.Color.parse('w'))
        self.assertEqual(Piece.Color.BLACK, Piece.Color.parse('b'))
        with self.assertRaises(ValueError):
            Piece.Color.parse('foo')

    def test_parse_type(self):
        self.assertEqual(Piece.Type.PAWN, Piece.Type.parse('p'))
        self.assertEqual(Piece.Type.BISHOP, Piece.Type.parse('b'))
        self.assertEqual(Piece.Type.KNIGHT, Piece.Type.parse('n'))
        self.assertEqual(Piece.Type.ROOK, Piece.Type.parse('r'))
        self.assertEqual(Piece.Type.QUEEN, Piece.Type.parse('q'))
        self.assertEqual(Piece.Type.KING, Piece.Type.parse('k'))
        with self.assertRaises(ValueError):
            Piece.Type.parse('foo')

    def test_parse(self):
        self.assertEqual(
            Piece(
                Piece.Color.BLACK,
                Piece.Type.QUEEN,
                Position.parse('f4'),
                True,
            ),
            Piece.parse('bqf4')
        )
        with self.assertRaises(ValueError):
            Piece.parse('foo')
