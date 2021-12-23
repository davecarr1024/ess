from board_tree import BoardTree

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import time


class StopCondition(ABC):
    def start(self) -> None: ...

    @abstractmethod
    def should_stop(self, num_samples: int) -> bool: ...


@dataclass(frozen=True)
class UntilNumSamples(StopCondition):
    max_num_samples: int

    def should_stop(self, num_samples: int) -> bool:
        return num_samples >= self.max_num_samples


@dataclass
class UntilTimeElapsed(StopCondition):
    max_time: float

    def start(self) -> None:
        self.start_time = time()

    def should_stop(self, num_samples: int) -> bool:
        return time() - self.start_time >= self.max_time


@dataclass(frozen=True)
class BoardTreeExpander(ABC):
    stop_condition: StopCondition

    def expand(self, board_tree: 'BoardTree') -> None:
        self.stop_condition.start()
        num_samples: int = 0
        candidates: list[BoardTree] = [board_tree]
        while not self.stop_condition.should_stop(num_samples):
            num_samples += 1
            candidate = self.select_candidate(candidates)
            candidates.remove(candidate)
            if candidate.can_expand():
                candidate.expand()
                self.add_candidates(candidate.children, candidates)

    @abstractmethod
    def select_candidate(self, candidates: list['BoardTree']) -> 'BoardTree':
        ...

    def add_candidates(self, candidates_to_add: list['BoardTree'], candidates: list['BoardTree']) -> None:
        candidates.extend(candidates_to_add)


class BFSExpander(BoardTreeExpander):
    def select_candidate(self, candidates: list['BoardTree']) -> 'BoardTree':
        return candidates[0]


class GreedyExpander(BoardTreeExpander):
    def select_candidate(self, candidates: list['BoardTree']) -> 'BoardTree':
        return max(candidates, key=lambda candidate: candidate.board_value)
