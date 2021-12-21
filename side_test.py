from side import Side
from unittest import TestCase


class SideTest(TestCase):
    def test_opponent(self):
        self.assertEqual(Side.WHITE.opponent(), Side.BLACK)
        self.assertEqual(Side.BLACK.opponent(), Side.WHITE)
