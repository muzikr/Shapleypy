from __future__ import annotations

import numpy as np
import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game

have_core = True

try:
    from shapleypy.solution_concept.core import (
        _get_payoff,
        contains_integer_point,
        get_vertices,
        is_empty,
        solution_in_core,
    )
except ImportError:
    have_core = False


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


@pytest.mark.skipif(not have_core, reason="pplpy is not installed")
def test_get_payoff() -> None:
    assert _get_payoff(Coalition.from_players([0]), np.array([1.0, 2.0])) == 1.0
    assert _get_payoff(Coalition.from_players([1]), np.array([1.0, 2.0])) == 2.0
    assert (
        _get_payoff(Coalition.from_players([0, 1]), np.array([1.0, 2.0])) == 3.0
    )


@pytest.mark.skipif(not have_core, reason="pplpy is not installed")
def test_solution_in_core() -> None:
    game = Game(2)
    game.set_value(Coalition.from_players([0]), 0.0)
    game.set_value(Coalition.from_players([1]), 0.0)
    game.set_value(Coalition.from_players([0, 1]), 1.0)
    assert solution_in_core(game, [0.5, 0.5])
    assert not solution_in_core(game, [0.5, 0.4])
    assert not solution_in_core(game, [1.0, 5.0])


@pytest.mark.skipif(not have_core, reason="pplpy is not installed")
def test_is_empty(
    game_of_three_values_non_empty_core: list[tuple[Coalition, float]],
    game_of_three_values_empty_core: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(game_of_three_values_non_empty_core)
    assert not is_empty(game)
    game.set_values(game_of_three_values_empty_core)
    assert is_empty(game)


@pytest.mark.skipif(not have_core, reason="pplpy is not installed")
def test_get_vertices(
    game_of_three_values_non_empty_core: list[tuple[Coalition, float]],
    game_of_three_values_empty_core: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(game_of_three_values_non_empty_core)
    assert set(get_vertices(game)) == {
        (0.25, 0.0, 0.75),
        (0.0, 0.5, 0.5),
        (0.25, 0.5, 0.25),
        (0.0, 0.25, 0.75),
    }
    game.set_values(game_of_three_values_empty_core)
    assert set(get_vertices(game)) == set()


@pytest.mark.skipif(not have_core, reason="pplpy is not installed")
def test_contain_integer_point(
    game_of_three_values_non_empty_core: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(game_of_three_values_non_empty_core)
    assert not contains_integer_point(game)
    game = Game(2)
    game.set_values(
        [
            (Coalition.from_players([0]), 0.0),
            (Coalition.from_players([1]), 0.0),
            (Coalition.from_players([0, 1]), 1.0),
        ]
    )
    assert contains_integer_point(game)
