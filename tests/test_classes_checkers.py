from __future__ import annotations

import pytest

from shapleypy.classes_checkers import (
    check_convexity,
    check_k_additivity,
    check_k_game,
    check_monotonicity,
    check_positivity,
    check_superadditivity,
    check_supermodularity,
    check_weakly_superadditivity,
    determine_class,
)
from shapleypy.coalition import Coalition
from shapleypy.game import Game


@pytest.fixture
def monotone_game_of_three() -> list[tuple[Coalition, float]]:
    """Not weakly superadditive"""
    return [
        (Coalition.from_players([0]), 6.0),
        (Coalition.from_players([1]), 12.0),
        (Coalition.from_players([0, 1]), 12.0),
        (Coalition.from_players([2]), 42.0),
        (Coalition.from_players([0, 2]), 42.0),
        (Coalition.from_players([1, 2]), 42.0),
        (Coalition.from_players([0, 1, 2]), 42.0),
    ]


@pytest.fixture
def positive_game_of_three() -> list[tuple[Coalition, float]]:
    """
    v(S)=|S|^2
    """
    return [
        (Coalition.from_players([0]), 1.0),
        (Coalition.from_players([1]), 1.0),
        (Coalition.from_players([0, 1]), 4.0),
        (Coalition.from_players([2]), 1.0),
        (Coalition.from_players([0, 2]), 4.0),
        (Coalition.from_players([1, 2]), 4.0),
        (Coalition.from_players([0, 1, 2]), 9.0),
    ]


@pytest.fixture
def k_game_of_three() -> list[tuple[Coalition, float]]:
    return [
        (Coalition.from_players([0]), 0.0),
        (Coalition.from_players([1]), 0.0),
        (Coalition.from_players([0, 1]), 1.0),
        (Coalition.from_players([2]), 0.0),
        (Coalition.from_players([0, 2]), 2.0),
        (Coalition.from_players([1, 2]), 3.0),
        (Coalition.from_players([0, 1, 2]), 6.0),
    ]


def test_check_monotonicity(
    monotone_game_of_three: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(monotone_game_of_three)
    assert check_monotonicity(game)
    game.set_value(Coalition.from_players([0, 2]), 10.0)
    assert not check_monotonicity(game)


def test_check_weakly_superadditivity(
    monotone_game_of_three: list[tuple[Coalition, float]],
    positive_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(monotone_game_of_three)
    assert not check_weakly_superadditivity(game)
    game.set_values(positive_game_of_three)
    assert check_weakly_superadditivity(game)


def test_check_superadditivity(
    positive_game_of_three: list[tuple[Coalition, float]],
    monotone_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(positive_game_of_three)
    assert check_superadditivity(game)
    game.set_values(monotone_game_of_three)
    assert not check_superadditivity(game)


def test_check_convexity(
    positive_game_of_three: list[tuple[Coalition, float]],
    monotone_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(positive_game_of_three)
    assert check_convexity(game)
    assert check_supermodularity(game)
    game.set_values(monotone_game_of_three)
    assert not check_convexity(game)
    assert not check_supermodularity(game)


def test_check_positivity(
    positive_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(positive_game_of_three)
    assert check_positivity(game)
    # For S={0, 1, 2}, m_S = 0 so if I set whole to 8 it will be -1
    game.set_value(Coalition.from_players([0, 1, 2]), 8.0)
    assert not check_positivity(game)


def test_detemine_class(
    positive_game_of_three: list[tuple[Coalition, float]],
    monotone_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(positive_game_of_three)
    assert determine_class(game) == "Positive"
    game.set_values(monotone_game_of_three)
    assert determine_class(game) == "Monotone"
    game.set_value(Coalition.from_players([0, 1, 2]), -8.0)
    assert determine_class(game) == "None"


def test_check_k_game(
    k_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(k_game_of_three)
    assert check_k_game(game, 2)
    assert not check_k_game(game, 1)
    assert check_k_game(game)


def test_check_k_additivity(
    positive_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(positive_game_of_three)
    assert check_k_additivity(game, 2)
    assert not check_k_additivity(game, 1)
