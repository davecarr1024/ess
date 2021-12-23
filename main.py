from board import Board
from board_tree_expander import BFSExpander, UntilNumSamples
from game import Game
from min_max_player import MinMaxPlayer
from piece import Piece
from piece_value_board_evaluator import PieceValueBoardEvalutor
from text_player import TextPlayer


def main():
    Game(
        TextPlayer(Piece.Color.WHITE),
        MinMaxPlayer(Piece.Color.BLACK,
                     PieceValueBoardEvalutor(Piece.Color.BLACK),
                     BFSExpander(UntilNumSamples(10))
                     )
    ).play(Board.default_board())


if __name__ == '__main__':
    main()
