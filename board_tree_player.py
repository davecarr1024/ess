from board import Board
from board_evaluator import BoardEvaluator
from board_tree import BoardTree
from board_tree_expander import BoardTreeExpander
from player import Player

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import time


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
        expansion_stats: BoardTreeExpander.Stats = self.board_tree_expander.expand(
            board_tree)
        start_time = time()
        child_results = [child.result for child in board_tree.children]
        max_child_result = max(child_results, key=lambda result: result.value)
        print(
            f'result boards {"".join([str(board) for board in max_child_result.boards])} stats {expansion_stats} at depth {len(max_child_result.boards)} with value {max_child_result.value} in {time() - start_time}')
        return max_child_result.boards[0]
