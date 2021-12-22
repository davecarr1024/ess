from board import Board
from piece import Piece

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BoardEvaluator(ABC):
    eval_color: Piece.Color

    @abstractmethod
    def evaluate(self, board: Board) -> float: ...
