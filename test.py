from abc import ABC, abstractmethod
from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum
from itertools import cycle
from typing import Generator, Optional, Sequence


@dataclass(frozen=True)
class Game(ABC):

    @dataclass(frozen=True)
    class Position:
        x: int
        y: int

    @dataclass(frozen=True)
    class Piece(ABC):
        player: 'Game.Player'
        position: 'Game.Position'

        @abstractmethod
        def with_position(self, position: 'Game.Position') -> 'Game.Piece': ...

        @abstractmethod
        def moves(self, board: 'Game.Board') -> Collection['Game.Board']: ...

    @dataclass(frozen=True)
    class Board:
        pieces: Collection['Game.Piece']

        def with_piece(self, piece: 'Game.Piece') -> 'Game.Board':
            pieces: list[Game.Piece] = [p for p in self.pieces]
            pieces.append(piece)
            return Game.Board(pieces)

        def without_piece(self, piece: 'Game.Piece') -> 'Game.Board':
            return Game.Board([p for p in self.pieces if p != piece])

        def with_piece_moved(self, piece: 'Game.Piece', to_position: 'Game.Position') -> 'Game.Board':
            board = self
            if to_position in board:
                board = board.without_piece(board[to_position])
            return board.without_piece(piece).with_piece(piece.with_position(to_position))

        def pieces_of_player(self, player: 'Game.Player') -> Collection['Game.Piece']:
            return [piece for piece in self.pieces if piece.player == player]

        def moves_of_player(self, player: 'Game.Player') -> Collection['Game.Board']:
            moves: list[Game.Board] = []
            return sum([piece.moves(self) for piece in self.pieces_of_player(player)], moves)

        def __contains__(self, position: 'Game.Position') -> bool:
            return any([piece.position == position for piece in self.pieces])

        def __getitem__(self, position: 'Game.Position') -> 'Game.Piece':
            for piece in self.pieces:
                if piece.position == position:
                    return piece
            raise KeyError(position)

    @dataclass(frozen=True)
    class Player(ABC):
        @abstractmethod
        def move(self, board: 'Game.Board') -> 'Game.Board': ...

    class Result:
        ...

    players: Sequence[Player]

    @abstractmethod
    def result(self, board: Board) -> Optional[Result]: ...

    def play(self, board: Board) -> Result:
        for player in cycle(self.players):
            board = player.move(board)
            result = self.result(board)
            if result is not None:
                return result
        raise RuntimeError()


class Chess(Game):
    @dataclass(frozen=True)
    class Position(Game.Position):

        @dataclass(frozen=True)
        class Delta:
            dx: int
            dy: int

            def __post_init__(self):
                assert self.dx in (-1, 0, 1)
                assert self.dy in (-1, 0, 1)

            def can_add(self, position: 'Game.Position') -> bool:
                return 0 <= position.x + self.dx < 8 and 0 <= position.y + self.dy < 8

            def __add__(self, position: 'Game.Position') -> 'Game.Position':
                return Chess.Position(position.x + self.dx, position.y + self.dy)

            def iter(self, position: 'Game.Position') -> Generator['Game.Position', None, None]:
                while self.can_add(position):
                    position = self + position
                    yield position

        def __post_init__(self):
            assert 0 <= self.x < 8
            assert 0 <= self.y < 8

        def __repr__(self) -> str:
            return f'{chr(self.x+ord("a"))}{self.y+1}'

        @staticmethod
        def parse(s: str) -> 'Chess.Position':
            assert len(s) == 2
            assert s[0] in 'abcdefgh'
            assert s[1] in '12345678'
            return Chess.Position(ord(s[0]) - ord('a'), int(s[1])-1)

    @dataclass(frozen=True)
    class LinearPiece(Game.Piece):
        @property
        @abstractmethod
        def deltas(self) -> Collection['Chess.Position.Delta']: ...

        def moves(self, board: Game.Board) -> Collection[Game.Board]:
            boards: list[Game.Board] = []
            for delta in self.deltas:
                for to_position in delta.iter(self.position):
                    if to_position not in board:
                        boards.append(
                            board.with_piece_moved(self, to_position))
                    else:
                        to_piece = board[to_position]
                        if to_piece.player != self.player:
                            boards.append(board.with_piece_moved(
                                self, to_position))
                        break
            return boards

    @dataclass(frozen=True)
    class Bishop(LinearPiece):
        @property
        def deltas(self) -> Collection['Chess.Position.Delta']:
            return (
                Chess.Position.Delta(1, 1),
                Chess.Position.Delta(1, -1),
                Chess.Position.Delta(-1, 1),
                Chess.Position.Delta(-1, -1),
            )

        def with_position(self, position: 'Game.Position') -> 'Game.Piece':
            return Chess.Bishop(self.player, position)

    @dataclass(frozen=True)
    class Player(Game.Player):
        class Side(Enum):
            WHITE = 1
            BLACK = 2

        side: Side

    class TextPlayer(Player):
        @staticmethod
        def get_position(prompt: str) -> 'Chess.Position':
            while True:
                try:
                    return Chess.Position.parse(input(prompt))
                except Exception as err:
                    print(f'input error: {type(err)}')

        def print_board(self, board: Game.Board) -> None:
            for y in range(7, -1, -1):
                print(f'{y+1} ', end='')
                for x in range(8):
                    pos = Chess.Position(x, y)
                    if pos in board:
                        piece = board[pos]
                        sym = piece.__class__.__name__[:1]
                        if piece.player == self:
                            sym = sym.upper()
                        else:
                            sym = sym.lower()
                        print(f'| {sym} ', end='')
                    else:
                        print('|   ', end='')
                print('|')
                print('-----------------------------------')
            print('  | a | b | c | d | e | f | g | h |')

        def move(self, board: Game.Board) -> Game.Board:
            while True:
                self.print_board(board)
                print(f'{self.side.name.lower()} player\'s move')
                from_position = self.get_position('move piece from what position? ')
                if from_position not in board:
                    print(f'no piece at {from_position}')
                    continue
                piece = board[from_position]
                if piece.player != self:
                    print(f'not your piece at {from_position}')
                    continue
                to_position = self.get_position(f'move {piece.__class__.__name__.lower()} to what position? ')
                new_board = board.with_piece_moved(piece, to_position)
                valid_moves = board.moves_of_player(self)
                if new_board not in board.moves_of_player(self):
                    print(f'invalid move: valid moves are {valid_moves}')
                    continue
                return new_board

    class Result(Game.Result, Enum):
        CHECKMATE = 1
        STALEMATE = 2

    def result(self, board: Game.Board) -> Optional[Result]:
        pass

    def default_board(self) -> 'Chess.Board':
        white = self.players[0]
        black = self.players[1]
        return Chess.Board([
            Chess.Bishop(white, Chess.Position.parse('c1')),
            Chess.Bishop(white, Chess.Position.parse('f1')),
            Chess.Bishop(black, Chess.Position.parse('c8')),
            Chess.Bishop(black, Chess.Position.parse('f8')),
        ])


if __name__ == '__main__':
    game = Chess([Chess.TextPlayer(Chess.Player.Side.WHITE),
                  Chess.TextPlayer(Chess.Player.Side.BLACK)])
    game.play(game.default_board())
