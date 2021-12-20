import dataclasses
import typing


@dataclasses.dataclass(frozen=True, repr=False)
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

        def enumerate(self, delta: Delta) -> typing.Generator['Position.Rank', None, None]:
            val = self
            while val.can_add(delta):
                val += delta
                yield val

    @dataclasses.dataclass(frozen=True)
    class File:
        @dataclasses.dataclass(frozen=True)
        class Delta:
            value: int

            def __post_init__(self):
                assert self.value in (-1, 0, 1)

            def __neg__(self) -> 'Position.File.Delta':
                return Position.File.Delta(-self.value)

        value: int

        def __post_init__(self):
            assert 1 <= self.value <= 8

        def can_add(self, delta: Delta) -> bool:
            return delta.value == 0 or (delta.value == -1 and self.value > 1
                                        ) or (delta.value == 1
                                              and self.value < 8)

        def __add__(self, delta: Delta) -> 'Position.File':
            assert self.can_add(delta)
            return Position.File(self.value + delta.value)

        def __sub__(self, delta: Delta) -> 'Position.File':
            return self + -delta

        def enumerate(self, delta: Delta) -> typing.Generator['Position.File', None, None]:
            val = self
            while val.can_add(delta):
                val += delta
                yield val

    @dataclasses.dataclass(frozen=True)
    class Delta:
        drank: 'Position.Rank.Delta'
        dfile: 'Position.File.Delta'

        def __neg__(self) -> 'Position.Delta':
            return Position.Delta(-self.drank, -self.dfile)

    rank: Rank
    file: File

    def __repr__(self) -> str:
        return f'{self.rank.value}{self.file.value}'

    @staticmethod
    def parse(s: str) -> 'Position':
        assert len(s) == 2
        return Position(Position.Rank(s[0]), Position.File(int(s[1])))

    @staticmethod
    def delta(drank: int, dfile: int) -> Delta:
        return Position.Delta(Position.Rank.Delta(drank), Position.File.Delta(dfile))

    def can_add(self, delta: Delta) -> bool:
        return self.rank.can_add(delta.drank) and self.file.can_add(delta.dfile)

    def __add__(self, delta: Delta) -> 'Position':
        assert self.can_add(delta)
        return Position(self.rank + delta.drank, self.file + delta.dfile)

    def __sub__(self, delta: Delta) -> 'Position':
        return self + -delta

    def enumerate(self, delta: Delta) -> typing.Generator['Position', None, None]:
        val = self
        while val.can_add(delta):
            val += delta
            yield val
