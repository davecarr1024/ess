from position import Position
from unittest import TestCase
from itertools import islice


class PositionRankDeltaTest(TestCase):
    def test_ctor(self):
        for val in (-1, 0, 1):
            with self.subTest(val=val):
                self.assertEqual(Position.Rank.Delta(val).value, val)

    def test_ctor_fail(self):
        with self.assertRaises(AssertionError):
            Position.Rank.Delta(2)

    def test_neg(self):
        self.assertEqual(-Position.Rank.Delta(1),
                         Position.Rank.Delta(-1))


class PositionRankTest(TestCase):
    def test_ctor_fail(self):
        with self.assertRaises(AssertionError):
            Position.Rank('i')

    def test_add(self):
        self.assertEqual(Position.Rank(
            'a') + Position.Rank.Delta(1), Position.Rank('b'))

    def test_add_fail(self):
        with self.assertRaises(AssertionError):
            Position.Rank('h') + Position.Rank.Delta(1)

    def test_sub(self):
        self.assertEqual(Position.Rank(
            'c') - Position.Rank.Delta(1), Position.Rank('b'))

    def test_enumerate_zero(self):
        self.assertListEqual(list(islice(Position.Rank('a').enumerate(
            Position.Rank.Delta(0)), 3)), [Position.Rank('a')]*3)

    def test_enumerate_right(self):
        self.assertListEqual(list(Position.Rank('f').enumerate(Position.Rank.Delta(1))),
                             [
                                 Position.Rank('g'),
                                 Position.Rank('h'),
        ]
        )

    def test_enumerate_left(self):
        self.assertListEqual(list(Position.Rank('c').enumerate(Position.Rank.Delta(-1))),
                             [
                                 Position.Rank('b'),
                                 Position.Rank('a'),
        ]
        )


class PositionFileDeltaTest(TestCase):
    def test_ctor(self):
        for val in (-1, 0, 1):
            with self.subTest(val=val):
                self.assertEqual(Position.File.Delta(val).value, val)

    def test_ctor_fail(self):
        with self.assertRaises(AssertionError):
            Position.File.Delta(2)

    def test_neg(self):
        self.assertEqual(-Position.File.Delta(1),
                         Position.File.Delta(-1))


class PositionFileTest(TestCase):
    def test_ctor_fail(self):
        with self.assertRaises(AssertionError):
            Position.File(9)

    def test_add(self):
        self.assertEqual(Position.File(
            1) + Position.File.Delta(1), Position.File(2))

    def test_add_fail(self):
        with self.assertRaises(AssertionError):
            Position.File(8) + Position.File.Delta(1)

    def test_sub(self):
        self.assertEqual(Position.File(
            3) - Position.File.Delta(1), Position.File(2))

    def test_enumerate_zero(self):
        self.assertListEqual(list(islice(Position.File(1).enumerate(
            Position.File.Delta(0)), 3)), [Position.File(1)]*3)

    def test_enumerate_right(self):
        self.assertListEqual(list(Position.File(6).enumerate(Position.File.Delta(1))),
                             [
                                 Position.File(7),
                                 Position.File(8),
        ]
        )

    def test_enumerate_left(self):
        self.assertListEqual(list(Position.File(3).enumerate(Position.File.Delta(-1))),
                             [
                                 Position.File(2),
                                 Position.File(1),
        ]
        )

    def test_enumerate_left_empty(self):
        self.assertListEqual(list(Position.File(
            1).enumerate(Position.File.Delta(-1))), [])


class PositionDeltaTest(TestCase):
    def test_neg(self):
        self.assertEqual(-Position.Delta(Position.Rank.Delta(1), Position.File.Delta(-1)),
                         Position.Delta(Position.Rank.Delta(-1), Position.File.Delta(1)))


class PositionTest(TestCase):
    def test_parse(self):
        self.assertEqual(Position.parse('c2'), Position(
            Position.Rank('c'), Position.File(2)))

    def test_delta(self):
        self.assertEqual(Position.delta(1, 0), Position.Delta(
            Position.Rank.Delta(1), Position.File.Delta(0)))

    def test_can_add(self):
        self.assertTrue(Position.parse('d8').can_add(Position.delta(1, 0)))
        self.assertFalse(Position.parse('d8').can_add(Position.delta(0, 1)))

    def test_add(self):
        self.assertEqual(Position.parse('d4') +
                         Position.delta(1, -1), Position.parse('e3'))

    def test_sub(self):
        self.assertEqual(Position.parse('d4') -
                         Position.delta(1, -1), Position.parse('c5'))

    def test_enumerate(self):
        self.assertListEqual(list(Position.parse('f4').enumerate(Position.delta(1, -1))),
                             [Position.parse('g3'), Position.parse('h2')])
