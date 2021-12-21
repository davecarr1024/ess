from position import Position

from unittest import TestCase


class PositionDeltaTest(TestCase):
    def test_neg(self):
        self.assertEqual(-Position.Delta(1, -1), Position.Delta(-1, 1))


class PositionTest(TestCase):
    def test_validate(self):
        with self.assertRaises(ValueError):
            Position(-1, -1)

    def test_can_add(self):
        self.assertTrue(Position(0, 0).can_add(Position.Delta(1, 0)))
        self.assertFalse(Position(0, 0).can_add(Position.Delta(-1, 0)))

    def test_add(self):
        self.assertEqual(Position(1, 2) + Position.Delta(3, 4), Position(4, 6))

    def test_sub(self):
        self.assertEqual(Position(3, 4) - Position.Delta(1, 2), Position(2, 2))

    def test_repr(self):
        self.assertEqual(repr(Position(2, 4)), 'c5')

    def test_parse(self):
        self.assertEqual(Position.parse('f2'), Position(5, 1))

    def test_parse_fail(self):
        for s in ['abc', 'z1', 'a9']:
            with self.subTest(s):
                with self.assertRaises(ValueError):
                    Position.parse(s)
