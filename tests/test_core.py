from __future__ import annotations

import numpy as np
import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.solution_concept.core import (
    _get_payoff,
    is_empty,
    solution_in_core,
)


@pytest.fixture
def game_of_three_values_non_empty_core() -> list[tuple[Coalition, float]]:
    return [
        (Coalition.from_players([0]), 0.0),
        (Coalition.from_players([1]), 0.0),
        (Coalition.from_players([0, 1]), 0.25),
        (Coalition.from_players([2]), 0.0),
        (Coalition.from_players([0, 2]), 0.5),
        (Coalition.from_players([1, 2]), 0.75),
        (Coalition.from_players([0, 1, 2]), 1.0),
    ]


@pytest.fixture
def game_of_three_values_empty_core() -> list[tuple[Coalition, float]]:
    return [
        (Coalition.from_players([0]), 0.0),
        (Coalition.from_players([1]), 0.0),
        (Coalition.from_players([0, 1]), 0.9),
        (Coalition.from_players([2]), 0.0),
        (Coalition.from_players([0, 2]), 0.9),
        (Coalition.from_players([1, 2]), 0.9),
        (Coalition.from_players([0, 1, 2]), 1.0),
    ]


def test_get_payoff() -> None:
    assert _get_payoff(Coalition.from_players([0]), np.array([1.0, 2.0])) == 1.0
    assert _get_payoff(Coalition.from_players([1]), np.array([1.0, 2.0])) == 2.0
    assert (
        _get_payoff(Coalition.from_players([0, 1]), np.array([1.0, 2.0])) == 3.0
    )


def test_solution_in_core() -> None:
    game = Game(2)
    game.set_value(Coalition.from_players([0]), 0.0)
    game.set_value(Coalition.from_players([1]), 0.0)
    game.set_value(Coalition.from_players([0, 1]), 1.0)
    assert solution_in_core(game, [0.5, 0.5])
    assert not solution_in_core(game, [0.5, 0.4])
    assert not solution_in_core(game, [1.0, 5.0])


def test_is_empty(
    game_of_three_values_non_empty_core: list[tuple[Coalition, float]],
    game_of_three_values_empty_core: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(game_of_three_values_non_empty_core)
    assert not is_empty(game)
    game.set_values(game_of_three_values_empty_core)
    assert is_empty(game)
