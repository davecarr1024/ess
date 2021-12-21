from board import Board
from player import Player
from position import Position


class TextPlayer(Player):
    @staticmethod
    def _get_position(prompt: str) -> Position:
        while True:
            try:
                return Position.parse(input(prompt))
            except Exception as err:
                print(f'failed to parse position: {err}')

    def move(self, board: Board) -> Board:
        while True:
            print(board)
            if board.is_color_in_check(self.color):
                print('you are in check!')
            from_position = self._get_position(
                f'player {self.color.name.lower()} select piece to move: ')
            from_piece = board.pieces_by_position.get(from_position, None)
            if from_piece is None:
                print(f'no piece at {from_position}')
                continue
            if from_piece.color != self.color:
                print(f'piece {from_piece} isn\'t yours')
                continue
            to_position = self._get_position(
                f'select destination for {from_piece}: ')
            new_board = board.with_piece_moved(from_piece, to_position)
            if new_board not in board.moves_for_color(self.color):
                print('invalid move')
                continue
            return new_board
