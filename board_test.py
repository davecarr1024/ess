from board import Board
from piece import Piece
from position import Position

from unittest import TestCase


class BoardTest(TestCase):
    @staticmethod
    def _piece(pos: str, type: Piece.Type = Piece.Type.PAWN, color: Piece.Color = Piece.Color.WHITE, has_moved: bool = False) -> Piece:
        return Piece(color, type, Position.parse(pos), has_moved)

    @staticmethod
    def _pos_board(*poss: str) -> Board:
        return BoardTest._board(*[BoardTest._piece(pos) for pos in poss])

    @staticmethod
    def _board(*pieces: Piece) -> Board:
        return Board(frozenset(pieces))

    def test_duplicate_positions(self):
        with self.assertRaises(ValueError):
            self._board(self._piece('c2', type=Piece.Type.BISHOP),
                        self._piece('c2', type=Piece.Type.KING))

    def test_with_piece(self):
        self.assertEqual(
            self._pos_board('c2').with_piece(self._piece('c3')),
            self._pos_board('c2', 'c3')
        )

    def test_without_piece(self):
        self.assertEqual(
            self._pos_board('c2', 'c3').without_piece(self._piece('c3')),
            self._pos_board('c2')
        )

    def test_with_piece_moved(self):
        self.assertEqual(
            self._pos_board('c2', 'c3').with_piece_moved(
                self._piece('c2'), Position.parse('c3')),
            self._board(self._piece('c3', has_moved=True))
        )

    def test_pieces_by_position(self):
        self.assertDictEqual(
            self._pos_board('c2', 'c3').pieces_by_position,
            {
                Position.parse('c2'): self._piece('c2'),
                Position.parse('c3'): self._piece('c3'),
            }
        )

    def test_pieces_by_color(self):
        p1 = self._piece('c3', color=Piece.Color.WHITE)
        p2 = self._piece('c4', color=Piece.Color.BLACK)
        self.assertDictEqual(
            self._board(p1, p2).pieces_by_color,
            {
                Piece.Color.WHITE: {p1},
                Piece.Color.BLACK: {p2},
            }
        )

    def test_pawn_initial_move(self):
        pawn = self._piece('c2', type=Piece.Type.PAWN, has_moved=False)
        self.assertSetEqual(
            self._board(pawn).moves_for_piece(pawn),
            {
                self._board(pawn.with_position(Position.parse('c3'))),
                self._board(pawn.with_position(Position.parse('c4'))),
            }
        )

    def test_pawn_subsequent_move(self):
        pawn = self._piece('c4', type=Piece.Type.PAWN, has_moved=True)
        self.assertSetEqual(
            self._board(pawn).moves_for_piece(pawn),
            {
                self._board(pawn.with_position(Position.parse('c5'))),
            }
        )

    def test_pawn_capture(self):
        for black_pawn_rank in ('b', 'd'):
            with self.subTest(black_pawn_rank=black_pawn_rank):
                white_pawn = self._piece(
                    'c3', type=Piece.Type.PAWN, color=Piece.Color.WHITE, has_moved=True)
                black_pawn = self._piece(
                    f'{black_pawn_rank}4', type=Piece.Type.PAWN, color=Piece.Color.BLACK, has_moved=True)
                self.assertSetEqual(
                    self._board(white_pawn, black_pawn).moves_for_piece(
                        white_pawn),
                    {
                        self._board(
                            white_pawn.with_position(Position.parse('c4')),
                            black_pawn),
                        self._board(
                            white_pawn.with_position(black_pawn.position)
                        ),
                    }
                )

    def test_bishop_move(self):
        bishop = self._piece('d4', type=Piece.Type.BISHOP,
                             color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(bishop).moves_for_piece(bishop),
            {
                self._board(bishop.with_position(Position.parse(pos)))
                for pos in
                ['c3', 'b2', 'a1', 'c5', 'b6', 'a7', 'e3',
                    'f2', 'g1', 'e5', 'f6', 'g7', 'h8']
            }
        )

    def test_bishop_stops_at_friend(self):
        bishop = self._piece('d4', type=Piece.Type.BISHOP,
                             color=Piece.Color.WHITE)
        friend = self._piece('b2', type=Piece.Type.PAWN,
                             color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(friend, bishop).moves_for_piece(bishop),
            {
                self._board(friend, bishop.with_position(Position.parse(pos)))
                for pos in
                ['c3', 'c5', 'b6', 'a7', 'e3',
                    'f2', 'g1', 'e5', 'f6', 'g7', 'h8']
            }
        )

    def test_bishop_captures_enemy(self):
        bishop = self._piece('d4', type=Piece.Type.BISHOP,
                             color=Piece.Color.WHITE)
        enemy = self._piece('b2', type=Piece.Type.PAWN,
                            color=Piece.Color.BLACK)
        self.assertSetEqual(
            self._board(enemy, bishop).moves_for_piece(bishop),
            {
                self._board(enemy, bishop.with_position(Position.parse(pos)))
                for pos in
                ['c3', 'c5', 'b6', 'a7', 'e3',
                    'f2', 'g1', 'e5', 'f6', 'g7', 'h8']
            }.union({self._board(bishop.with_position(enemy.position))})
        )

    def test_rook_move(self):
        rook = self._piece('d4', type=Piece.Type.ROOK, color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(rook).moves_for_piece(rook),
            {
                self._board(rook.with_position(Position.parse(pos)))
                for pos in ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4', 'd1', 'd2', 'd3', 'd5', 'd6', 'd7', 'd8']
            }
        )

    def test_rook_stops_at_friend(self):
        rook = self._piece('d4', type=Piece.Type.ROOK, color=Piece.Color.WHITE)
        friend = self._piece('d2', type=Piece.Type.PAWN,
                             color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(friend, rook).moves_for_piece(rook),
            {
                self._board(friend, rook.with_position(Position.parse(pos)))
                for pos in ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4', 'd3', 'd5', 'd6', 'd7', 'd8']
            }
        )

    def test_rook_captures_enemy(self):
        rook = self._piece('d4', type=Piece.Type.ROOK, color=Piece.Color.WHITE)
        enemy = self._piece('d2', type=Piece.Type.PAWN,
                            color=Piece.Color.BLACK)
        self.assertSetEqual(
            self._board(enemy, rook).moves_for_piece(rook),
            {
                self._board(enemy, rook.with_position(Position.parse(pos)))
                for pos in ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4', 'd3', 'd5', 'd6', 'd7', 'd8']
            }.union({self._board(rook.with_position(enemy.position))})
        )

    def test_queen_move(self):
        queen = self._piece('d4', type=Piece.Type.QUEEN,
                            color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(queen).moves_for_piece(queen),
            {
                self._board(queen.with_position(Position.parse(pos)))
                for pos in ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4', 'd1', 'd2', 'd3', 'd5', 'd6', 'd7', 'd8', 'c3', 'b2', 'a1', 'c5', 'b6', 'a7', 'e3',
                            'f2', 'g1', 'e5', 'f6', 'g7', 'h8']
            }
        )

    def test_queen_stops_at_friend(self):
        queen = self._piece('d4', type=Piece.Type.QUEEN,
                            color=Piece.Color.WHITE)
        friend = self._piece('b2', type=Piece.Type.PAWN,
                             color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(friend, queen).moves_for_piece(queen),
            {
                self._board(friend, queen.with_position(Position.parse(pos)))
                for pos in ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4', 'd1', 'd2', 'd3', 'd5', 'd6', 'd7', 'd8', 'c3', 'c5', 'b6', 'a7', 'e3',
                            'f2', 'g1', 'e5', 'f6', 'g7', 'h8']
            }
        )

    def test_queen_captures_enemy(self):
        queen = self._piece('d4', type=Piece.Type.QUEEN,
                            color=Piece.Color.WHITE)
        enemy = self._piece('b2', type=Piece.Type.PAWN,
                            color=Piece.Color.BLACK)
        self.assertSetEqual(
            self._board(enemy, queen).moves_for_piece(queen),
            {
                self._board(enemy, queen.with_position(Position.parse(pos)))
                for pos in ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4', 'd1', 'd2', 'd3', 'd5', 'd6', 'd7', 'd8', 'c3', 'c5', 'b6', 'a7', 'e3',
                            'f2', 'g1', 'e5', 'f6', 'g7', 'h8']
            }.union({self._board(queen.with_position(enemy.position))})
        )

    def test_king_move(self):
        king = self._piece('d4', type=Piece.Type.KING, color=Piece.Color.WHITE)
        self.assertSetEqual(
            self._board(king).moves_for_piece(king),
            {
                self._board(king.with_position(Position.parse(pos)))
                for pos in ['c3', 'c4', 'c5', 'd3', 'd5', 'e3', 'e4', 'e5']
            }
        )

    def test_king_captures_enemy(self):
        king = self._piece('d4', type=Piece.Type.KING, color=Piece.Color.WHITE)
        enemy = self._piece('d5', type=Piece.Type.PAWN,
                            color=Piece.Color.BLACK)
        self.assertSetEqual(
            self._board(enemy, king).moves_for_piece(king),
            {
                self._board(enemy, king.with_position(Position.parse(pos)))
                for pos in ['c3', 'c4', 'c5', 'd3', 'e3', 'e4', 'e5']
            }.union({self._board(king.with_position(enemy.position))})
        )

    def test_knight_move(self):
        knight = self._piece('d4', type=Piece.Type.KNIGHT,
                             color=Piece.Color.WHITE)
        pawns = [self._piece(pos, type=Piece.Type.PAWN, color=Piece.Color.WHITE) for pos in [
            'c3', 'c4', 'c5', 'd3', 'e3', 'e4', 'e5']]
        self.assertSetEqual(
            self._board(knight, *pawns).moves_for_piece(knight),
            {
                self._board(knight.with_position(Position.parse(pos)), *pawns)
                for pos in ['c2', 'e2', 'f3', 'f5', 'e6', 'c6', 'b5', 'b3']
            }
        )

    def test_knight_captures_enemy(self):
        knight = self._piece('d4', type=Piece.Type.KNIGHT,
                             color=Piece.Color.WHITE)
        pawns = [self._piece(pos, type=Piece.Type.PAWN, color=Piece.Color.WHITE) for pos in [
            'c3', 'c4', 'c5', 'd3', 'e3', 'e4', 'e5']]
        enemy = self._piece('e6', type=Piece.Type.PAWN,
                            color=Piece.Color.BLACK)
        self.assertSetEqual(
            self._board(knight, enemy, *pawns).moves_for_piece(knight),
            {
                self._board(enemy, knight.with_position(
                    Position.parse(pos)), *pawns)
                for pos in ['c2', 'e2', 'f3', 'f5', 'c6', 'b5', 'b3']
            }.union({self._board(knight.with_position(enemy.position), *pawns)})
        )

    def test_moves_for_color(self):
        white_pieces = [
            self._piece('a1', type=Piece.Type.ROOK, color=Piece.Color.WHITE),
            self._piece('b1', type=Piece.Type.KNIGHT, color=Piece.Color.WHITE),
            self._piece('c1', type=Piece.Type.BISHOP, color=Piece.Color.WHITE),
            self._piece('d1', type=Piece.Type.QUEEN, color=Piece.Color.WHITE),
            self._piece('e1', type=Piece.Type.KING, color=Piece.Color.WHITE),
        ]
        black_pieces = [
            self._piece('a8', type=Piece.Type.ROOK, color=Piece.Color.BLACK),
            self._piece('b8', type=Piece.Type.KNIGHT, color=Piece.Color.BLACK),
            self._piece('c8', type=Piece.Type.BISHOP, color=Piece.Color.BLACK),
            self._piece('d8', type=Piece.Type.QUEEN, color=Piece.Color.BLACK),
            self._piece('e8', type=Piece.Type.KING, color=Piece.Color.BLACK),
        ]
        board = self._board(*(white_pieces + black_pieces))
        boards: set[Board] = set()
        self.assertSetEqual(
            board.moves_for_color(Piece.Color.WHITE),
            boards.union(*[board.moves_for_piece(piece)
                           for piece in white_pieces])
        )

    def test_threatened(self):
        white_king = self._piece(
            'e1', type=Piece.Type.KING, color=Piece.Color.WHITE)
        black_rook = self._piece(
            'e4', type=Piece.Type.ROOK, color=Piece.Color.BLACK)
        self.assertTrue(self._board(
            white_king, black_rook).is_piece_threatened(white_king))
        self.assertFalse(self._board(
            white_king, black_rook.with_position(Position.parse('h4'))).is_piece_threatened(white_king))

    def test_king_for_color(self):
        with self.assertRaises(ValueError):
            self._board().king_for_color(Piece.Color.WHITE)
        white_king = self._piece(
            'e1', type=Piece.Type.KING, color=Piece.Color.WHITE)
        black_king = self._piece(
            'e8', type=Piece.Type.KING, color=Piece.Color.BLACK)
        self.assertEqual(self._board(white_king, black_king).king_for_color(
            Piece.Color.WHITE), white_king)

    def test_is_color_in_check(self):
        white_king = self._piece(
            'e1', type=Piece.Type.KING, color=Piece.Color.WHITE)
        black_rook = self._piece(
            'e4', type=Piece.Type.ROOK, color=Piece.Color.BLACK)
        self.assertTrue(self._board(
            white_king, black_rook).is_color_in_check(Piece.Color.WHITE))
        self.assertFalse(self._board(
            white_king.with_position(Position.parse('d1')), black_rook).is_color_in_check(Piece.Color.WHITE))


if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999
