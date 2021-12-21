from board import Board
from game import Game
from piece import Piece
from text_player import TextPlayer


def main():
    Game(
        TextPlayer(Piece.Color.WHITE),
        TextPlayer(Piece.Color.BLACK)
    ).play(Board.default_board())


if __name__ == '__main__':
    main()
