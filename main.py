from board import Board
from board_tree_expander import *
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
                     WeightedRandomExpander(UntilTime(30))
                     )
    ).play(Board.parse('bke8,bra8,brh8,wke1', False))


if __name__ == '__main__':
    main()
