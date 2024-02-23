from __future__ import annotations

import pytest

from shapleypy.coalition import Coalition
from shapleypy.constants import DEFAULT_VALUE
from shapleypy.game import Game
from shapleypy.solution_concept.shapley_value import (
    shapley,
    shapley_value_of_game,
    shapley_value_of_player,
)


@pytest.fixture
def basic_values_for_game_of_three() -> list[tuple[Coalition, float]]:
    return [
        (Coalition.from_players([0]), 1.0),
        (Coalition.from_players([1]), 2.0),
        (Coalition.from_players([0, 1]), 3.0),
        (Coalition.from_players([2]), 4.0),
        (Coalition.from_players([0, 2]), 5.0),
        (Coalition.from_players([1, 2]), 6.0),
        (Coalition.from_players([0, 1, 2]), 7.0),
    ]


@pytest.fixture
def basic_values_for_game_of_three_with_missing_values() -> (
    list[tuple[Coalition, float]]
):
    return [
        (Coalition.from_players([0]), 1.0),
        (Coalition.from_players([1]), 2.0),
        (Coalition.from_players([0, 2]), 7.0),
        (Coalition.from_players([1, 2]), 6.0),
        (Coalition.from_players([0, 1, 2]), 7.0),
    ]


def test_shapley_value_of_player(
    basic_values_for_game_of_three: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three)
    assert shapley_value_of_player(game, 0) == 1.0
    assert shapley_value_of_player(game, 1) == 2.0
    assert shapley_value_of_player(game, 2) == 4.0


def test_shapley_value_of_game(
    basic_values_for_game_of_three: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three)
    assert list(shapley_value_of_game(game)) == [1.0, 2.0, 4.0]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_shapley_value_of_game_with_default_value(
    basic_values_for_game_of_three_with_missing_values: list[
        tuple[Coalition, float]
    ]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_with_missing_values)
    assert list(shapley_value_of_game(game)) == [1.5, 1.5, 4.0]


def test_shapley_value_of_game_with_default_value_warning(
    basic_values_for_game_of_three_with_missing_values: list[
        tuple[Coalition, float]
    ]
) -> None:
    """
    If user did not set the default value parameter, he probably missed a
    value and should get a warning.
    """
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_with_missing_values)
    with pytest.warns(RuntimeWarning):
        list(shapley_value_of_game(game))


def test_shapley_value_of_game_with_default_value_without_warning(
    basic_values_for_game_of_three_with_missing_values: list[
        tuple[Coalition, float]
    ]
) -> None:
    """
    If user set the default value parameter to the default value, he probably
    knows what he is doing and should not get warining.
    """
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_with_missing_values)
    assert list(shapley_value_of_game(game, DEFAULT_VALUE)) == [1.5, 1.5, 4.0]


def test_shapley_value_of_game_with_set_default_value(
    basic_values_for_game_of_three_with_missing_values: list[
        tuple[Coalition, float]
    ]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_with_missing_values)
    assert list(shapley_value_of_game(game, 5.0)) == [1.5, 1.5, 4.0]


def test_shapley_function(
    basic_values_for_game_of_three: list[tuple[Coalition, float]],
    basic_values_for_game_of_three_with_missing_values: list[
        tuple[Coalition, float]
    ],
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three)
    assert list(shapley(game)) == [1.0, 2.0, 4.0]  # type: ignore
    assert shapley(game, 0) == 1.0
    assert shapley(game, 1) == 2.0
    assert shapley(game, 2) == 4.0
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_with_missing_values)
    assert list(shapley(game, default_value=5.0)) == [1.5, 1.5, 4.0]  # type: ignore
