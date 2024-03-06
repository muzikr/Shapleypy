from __future__ import annotations

import pytest

from shapleypy.classes.checkers import (
    check_monotone,
    check_weakly_superadditive,
)
from shapleypy.coalition import Coalition
from shapleypy.game import Game


@pytest.fixture
def monotone_game_of_three() -> list[tuple[Coalition, float]]:
    """Not weakly superadditive."""
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


def test_check_monotone(
    monotone_game_of_three: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(monotone_game_of_three)
    assert check_monotone(game)
    game.set_value(Coalition.from_players([0, 2]), 10.0)
    assert not check_monotone(game)


def test_check_weakly_superadditive(
    monotone_game_of_three: list[tuple[Coalition, float]],
    superadditive_game_of_three: list[tuple[Coalition, float]],
) -> None:
    game = Game(3)
    game.set_values(monotone_game_of_three)
    assert not check_weakly_superadditive(game)
    game.set_values(superadditive_game_of_three)
    assert check_weakly_superadditive(game)