# ruff: noqa: N806, B008
from __future__ import annotations

from enum import Enum

import numpy as np

from shapleypy.game import Game


class ReturnType(Enum):
    FLOAT = 1
    INTEGER = 2


def _generate_random(
    generator: np.random.Generator,
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
) -> float:
    """
    generator must implement random (return floats between 0 and 1)
    and integers (returns integer between lower and uper bound) methods.
    """
    return (
        generator.integers(lower_bound, upper_bound)
        if return_type == ReturnType.INTEGER
        else generator.integers(lower_bound, upper_bound) + generator.random()
    )


def random_game_generator(
    number_of_players: int,
    generator: np.random.Generator = np.random.default_rng(),
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
) -> Game:
    game = Game(number_of_players)

    for S in game.all_coalitions:
        random_number = _generate_random(
            generator, return_type, lower_bound, upper_bound
        )
        game.set_value(S, random_number)

    return game
