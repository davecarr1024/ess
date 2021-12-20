import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class Position:
    @dataclasses.dataclass(frozen=True)
    class Rank:
        @dataclasses.dataclass(frozen=True)
        class Delta:
            value: int

            def __post_init__(self):
                assert self.value in (-1, 0, 1)

            def __neg__(self) -> 'Position.Rank.Delta':
                return Position.Rank.Delta(-self.value)

            @staticmethod
            def test():
                assert Position.Rank.Delta(-1).value == -1
                assert -Position.Rank.Delta(-1) == Position.Rank.Delta(1)

        value: str

        def __post_init__(self):
            assert self.value in 'abcdefgh'

        def can_add(self, delta: Delta) -> bool:
            return delta.value == 0 or (delta.value == -1 and self.value > 'a'
                                        ) or (delta.value == 1
                                              and self.value < 'h')

        def __add__(self, delta: Delta) -> 'Position.Rank':
            assert self.can_add(delta)
            return Position.Rank(chr(ord(self.value) + delta.value))

        def __sub__(self, delta: Delta) -> 'Position.Rank':
            return self + -delta

        def enumerate(self, delta: Delta) -> typing.List['Position.Rank']:
            pass

        @staticmethod
        def test():
            assert Position.Rank('a').can_add(Position.Rank.Delta(0))
            assert Position.Rank('a').can_add(Position.Rank.Delta(1))
            assert not Position.Rank('a').can_add(Position.Rank.Delta(-1))
            assert Position.Rank('d') + Position.Rank.Delta(
                1) == Position.Rank('e')
            assert Position.Rank('d') + Position.Rank.Delta(
                0) == Position.Rank('d')
            assert Position.Rank('d') + Position.Rank.Delta(
                -1) == Position.Rank('c')

    file: str
    rank: int

    def __post__init__(self):
        assert self.file in 'abcdefgh'
        assert 1 <= self.rank <= 8

    @staticmethod
    def parse(s: str) -> 'Position':
        return Position(s[0], int(s[1]))

    @staticmethod
    def test():
        Position.Rank.test()
        assert Position.parse('a1') == Position('a', 1)
