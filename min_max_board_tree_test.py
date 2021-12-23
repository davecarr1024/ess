from board import Board
from min_max_board_tree import MinMaxBoardTree
from piece import Piece
from piece_value_board_evaluator import PieceValueBoardEvalutor

from unittest import TestCase


class MinMaxBoardTreeTest(TestCase):
    def test_boards(self):
        def case(start_board: str, end_board: str, depth: int) -> None:
            with self.subTest((start_board, end_board, depth)):
                bt = MinMaxBoardTree(
                    Board.parse(start_board),
                    PieceValueBoardEvalutor(Piece.Color.WHITE),
                    Piece.Color.WHITE,
                )
                bt.expand_to_depth(depth)
                self.assertEqual(
                    Board.parse(end_board),
                    bt.result.boards[-1],
                    f'{bt}\n{bt.result}'
                )
        case('wpe2,bpd5', 'wpd4', 5)
