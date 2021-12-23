from board_tree_expander import BFSExpander, UntilTime
from piece import Piece
from piece_value_board_evaluator import PieceValueBoardEvalutor
from min_max_player import MinMaxPlayer

from unittest import TestCase


class MinMaxPlayerTest(TestCase):
    def test_evaluator_color_mismatch(self):
        with self.assertRaises(ValueError):
            MinMaxPlayer(Piece.Color.WHITE,
                         PieceValueBoardEvalutor(Piece.Color.BLACK),
                         BFSExpander(UntilTime(10))
                         )
