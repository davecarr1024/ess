from board_tree import BoardTree
from weighted_random_choice import weighted_random_choice

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import time


class StopCondition(ABC):
    def start(self) -> None: ...

    @abstractmethod
    def should_stop(self, num_samples: int,
                    candidates: list['BoardTree']) -> bool: ...


@dataclass(frozen=True)
class UntilNumSamples(StopCondition):
    max_num_samples: int

    def should_stop(self, num_samples: int, candidates: list['BoardTree']) -> bool:
        return num_samples >= self.max_num_samples


@dataclass
class UntilTime(StopCondition):
    max_time: float

    def start(self) -> None:
        self.start_time = time()

    def should_stop(self, num_samples: int, candidates: list['BoardTree']) -> bool:
        return time() - self.start_time >= self.max_time


@dataclass(frozen=True)
class UntilDepth(StopCondition):
    max_depth: int

    def should_stop(self, num_samples: int, candidates: list['BoardTree']) -> bool:
        return any([candidate.depth > self.max_depth for candidate in candidates])


@dataclass(frozen=True)
class BoardTreeExpander(ABC):
    stop_condition: StopCondition

    @dataclass(frozen=True)
    class Stats:
        num_samples: int
        num_expansions: int
        total_time: float

    def expand(self, board_tree: 'BoardTree') -> 'BoardTreeExpander.Stats':
        self.stop_condition.start()
        start_time: float = time()
        num_samples: int = 0
        num_expansions: int = 0
        candidates: list[BoardTree] = [board_tree]
        while candidates and not self.stop_condition.should_stop(num_samples, candidates):
            num_samples += 1
            candidate = self.select_candidate(candidates)
            candidates.remove(candidate)
            if candidate.can_expand():
                candidate.expand()
                num_expansions += len(candidate.children)
                self.add_candidates(candidate.children, candidates)
        return BoardTreeExpander.Stats(num_samples, num_expansions, time()-start_time)

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


class WeightedRandomExpander(BoardTreeExpander):
    def select_candidate(self, candidates: list['BoardTree']) -> 'BoardTree':
        return weighted_random_choice([(candidate, candidate.board_value) for candidate in candidates])
