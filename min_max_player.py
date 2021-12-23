from board import Board
from board_tree import BoardTree
from board_tree_player import BoardTreePlayer
from min_max_board_tree import MinMaxBoardTree


class MinMaxPlayer(BoardTreePlayer):
    def board_tree(self, board: Board) -> BoardTree:
        board_tree = MinMaxBoardTree(board, self.board_evaluator, self.color)
        return board_tree
