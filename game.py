from board import Board
from piece import Piece
from player import Player

from dataclasses import dataclass
from enum import Enum
from itertools import cycle


@dataclass
class Game:
    white_player: Player
    black_player: Player

    @dataclass
    class Result:

        class Type(Enum):
            CHECKMATE = 1

        type: Type
        color: Piece.Color

    def __post_init__(self):
        if self.white_player.color != Piece.Color.WHITE or self.black_player.color != Piece.Color.BLACK:
            raise ValueError(self)

    def play(self, board: Board) -> 'Game.Result':
        for player in cycle((self.white_player, self.black_player)):
            for color in Piece.Color:
                if board.is_color_in_checkmate(color):
                    return Game.Result(Game.Result.Type.CHECKMATE, color)
            board = player.move(board)
        raise RuntimeError()
