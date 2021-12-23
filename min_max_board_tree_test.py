from board import Board
from min_max_board_tree import MinMaxBoardTree
from piece import Piece
from piece_value_board_evaluator import PieceValueBoardEvalutor

from unittest import TestCase


class MinMaxBoardTreeTest(TestCase):
    def test_boards(self):
        def case(start_board: str, result_boards: list[str], depth: int) -> None:
            with self.subTest((start_board, result_boards, depth)):
                bt = MinMaxBoardTree(
                    Board.parse(start_board),
                    PieceValueBoardEvalutor(Piece.Color.WHITE),
                    Piece.Color.WHITE,
                )
                bt.expand_to_depth(depth)
                self.assertListEqual(
                    [Board.parse(board) for board in result_boards],
                    bt.result.boards[1:][:len(result_boards)],
                    f'{bt}\n{bt.result}'
                )
        # capture a piece instead of moving
        case('wpe4,bpd5', ['wpd5'], 1)
        # capture the more valuable piece
        case('wpe4,bpd5,bnf5', ['bpd5,wpf5'], 1)
        # avoid attack
        case('wpe4,wpg2,bra4', ['wpe5,wpg2,bra4'], 2)
