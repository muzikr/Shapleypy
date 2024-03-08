from __future__ import annotations

import pytest

from shapleypy.classes.checkers import (
    check_convexity,
    check_monotonicity,
    check_positivity,
    check_superadditivity,
    check_supermodularity,
    check_weakly_superadditivity,
)
from shapleypy.coalition import Coalition
from shapleypy.game import Game


@pytest.fixture
def monotone_game_of_three() -> list[tuple[Coalition, float]]:
    """Not weakly superadditive, not supperadditive, not convex"""
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
def superadditive_game_of_three() -> list[tuple[Coalition, float]]:
    """Superadditive, weakly superadditive"""
    return [
        (Coalition.from_players([0]), 6.0),
        (Coalition.from_players([1]), 12.0),
        (Coalition.from_players([0, 1]), 18.0),
        (Coalition.from_players([2]), 42.0),
        (Coalition.from_players([0, 2]), 48.0),
        (Coalition.from_players([1, 2]), 55.0),
        (Coalition.from_players([0, 1, 2]), 80.0),
    ]


@pytest.fixture
def convex_game_of_three() -> list[tuple[Coalition, float]]:
    """
    Superadditive, weakly superadditive, convex, positive
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
    superadditive_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(monotone_game_of_three)
    assert not check_weakly_superadditivity(game)
    game.set_values(superadditive_game_of_three)
    assert check_weakly_superadditivity(game)


def test_check_superadditivity(
    superadditive_game_of_three: list[tuple[Coalition, float]],
    monotone_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(superadditive_game_of_three)
    assert check_superadditivity(game)
    game.set_values(monotone_game_of_three)
    assert not check_superadditivity(game)


def test_check_convexity(
    convex_game_of_three: list[tuple[Coalition, float]],
    monotone_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(convex_game_of_three)
    assert check_convexity(game)
    assert check_supermodularity(game)
    game.set_values(monotone_game_of_three)
    assert not check_convexity(game)
    assert not check_supermodularity(game)


def test_check_positivity(
    convex_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(convex_game_of_three)
    assert check_positivity(game)
    # For S={0, 1, 2}, m_S = 0 so if I set whole to 8 it will be -1
    game.set_value(Coalition.from_players([0, 1, 2]), 8.0)
    assert not check_positivity(game)
