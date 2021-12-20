import unittest

class PositionTest:
    def test_rank_delta_value(self):
        self.assertEqual(Position.Rank.Delta(-1).value, -1)

if __name__ == '__main__':
    unittest.main()
