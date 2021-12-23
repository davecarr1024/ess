from collections.abc import MutableSequence
import random
from typing import Tuple, TypeVar

T = TypeVar('T')


def weighted_random_choice(choices: MutableSequence[Tuple[T, float]]) -> T:
    weights = [t[1] for t in choices]
    if any([weight < 0 for weight in weights]):
        min_weight = min(weights)

        def normalize_weight(weight: float) -> float:
            return weight-min_weight+1
        choices = [(choice, normalize_weight(weight))
                   for choice, weight in choices]
    random_cum_weight: float = random.uniform(0, sum([t[1] for t in choices]))
    cum_weight: float = 0
    val: T
    weight: float
    random.shuffle(choices)
    for val, weight in choices:
        cum_weight += weight
        if cum_weight >= random_cum_weight:
            return val
    raise RuntimeError()
