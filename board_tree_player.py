from board import Board
from board_evaluator import BoardEvaluator
from board_tree import BoardTree
from board_tree_expander import BoardTreeExpander
from player import Player

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class BoardTreePlayer(Player, ABC):
    board_evaluator: BoardEvaluator
    board_tree_expander: BoardTreeExpander

    def __post_init__(self):
        if not self.color == self.board_evaluator.eval_color:
            raise ValueError((self.color, self.board_evaluator.eval_color))

    @abstractmethod
    def board_tree(self, board: Board) -> BoardTree: ...

    def move(self, board: Board) -> Board:
        print(f'{self} player considering board {board}')
        board_tree = self.board_tree(board)
        self.board_tree_expander.expand(board_tree)
        return board_tree.max_child.board
