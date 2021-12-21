from dataclasses import dataclass

@dataclass(frozen=True)
class Position:

    @dataclass(frozen=True)
    class Delta:
        dx: int
        dy: int

        def __neg__(self) -> 'Position.Delta':
            return Position.Delta(-self.dx, -self.dy)

    x: int
    y: int

    def __post_init__(self):
        if self.x < 0 or self.x >= 8 or self.y < 0 or self.y >= 8:
            raise ValueError(self)

    def can_add(self, d: 'Position.Delta') -> bool:
        return 0 <= self.x + d.dx < 8 and 0 <= self.y + d.dy < 8

    def __add__(self, d: 'Position.Delta') -> 'Position':
        if not self.can_add(d):
            raise ValueError(self, d)
        return Position(self.x + d.dx, self.y + d.dy)

    def __sub__(self, d: 'Position.Delta') -> 'Position':
        return self + -d

    def __repr__(self) -> str:
        return f'{chr(ord("a")+self.x)}{self.y+1}'

    @staticmethod
    def parse(s: str) -> 'Position':
        if len(s) != 2 or s[0] not in 'abcdefgh' or s[1] not in '12345678':
            raise ValueError(s)
        return Position(ord(s[0])-ord('a'), int(s[1])-1)
