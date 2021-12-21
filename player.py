from board import Board
from piece import Piece

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Player(ABC):
    color: Piece.Color

    @abstractmethod
    def move(self, board: Board) -> Board: ...
