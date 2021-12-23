from board import Board
from board_evaluator import BoardEvaluator
from board_tree import BoardTree
from piece import Piece


class MinMaxBoardTree(BoardTree):
    @property
    def result(self) -> BoardTree.Result:
        if not self.children:
            return BoardTree.Result([self.board], self.board_value)
        child_results: list[BoardTree.Result] = [child.result
                                                 for child in self.children]
        child_result = (max if self.color == self.board_evaluator.eval_color else min)(
            child_results, key=lambda result: result.value)
        return child_result.with_parent_board(self.board)

    def create_child(self, board: Board,
                     board_evaluator: BoardEvaluator,
                     color: Piece.Color,
                     depth: int) -> 'BoardTree':
        return MinMaxBoardTree(board, board_evaluator, color, depth)
