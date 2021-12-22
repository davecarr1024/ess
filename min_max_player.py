from board import Board
from board_evaluator import BoardEvaluator
from piece import Piece
from player import Player

from collections.abc import Collection
from dataclasses import dataclass, field
from functools import cached_property
from time import time


@dataclass(frozen=True)
class MinMaxPlayer(Player):
    board_evaluator: BoardEvaluator

    def __post_init__(self):
        if not self.color == self.board_evaluator.eval_color:
            raise ValueError((self.color, self.board_evaluator.eval_color))

    @dataclass
    class Node:
        board_evaluator: BoardEvaluator
        color: Piece.Color
        board: Board
        depth: int = 0
        children: Collection['MinMaxPlayer.Node'] = field(default_factory=list)

        def __str__(self) -> str:
            return f'node for {self.color.name} at {self.depth} with local {self.signed_board_value} {self.board}'

        def expand(self):
            if not self.board.is_color_in_checkmate(self.color):
                self.children = [
                    MinMaxPlayer.Node(
                        self.board_evaluator,
                        self.color.opponent,
                        board,
                        self.depth + 1,
                    )
                    for board in self.board.moves_for_color(self.color)
                ]

        @cached_property
        def board_value(self) -> float:
            return self.board_evaluator.evaluate(self.board)

        @property
        def signed_board_value(self) -> float:
            return (-1 if self.color != self.board_evaluator.eval_color else 1) * self.board_value

        @cached_property
        def value(self) -> float:
            if not self.children:
                return self.board_value
            child_values: list[float] = [child.value
                                         for child in self.children]
            if self.color == self.board_evaluator.eval_color:
                return max(child_values)
            else:
                return min(child_values)

    def expand(self, node: 'MinMaxPlayer.Node', steps: int = 100) -> None:
        nodes = [node]
        start = time()
        num_expansions = 0
        num_chlidren = 0
        # while time() < start + max_time:
        for _ in range(steps):
            num_expansions += 1
            # node = max(nodes, key=lambda node: node.signed_board_value)
            node = nodes[0]
            nodes.remove(node)
            node.expand()
            nodes.extend(node.children)
            num_chlidren += len(node.children)
            # for child in node.children:
            #     print(f'expanded {child}')
        print(
            f'expanded {num_expansions} nodes with {num_chlidren} children in {time() - start}')

    def move(self, board: Board) -> Board:
        print(f'minmax player {self.color.name} considering board {board}')
        node = MinMaxPlayer.Node(self.board_evaluator, self.color, board)
        self.expand(node)
        start = time()
        move_node = max(node.children, key=lambda node: node.value)
        print(
            f'chose move with {move_node.value} in {time() - start}')
        return move_node.board
