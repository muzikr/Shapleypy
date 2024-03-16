from __future__ import annotations

import sys

import pytest

from shapleypy.classes_checkers import (
    check_convexity,
    check_k_additivity,
    check_k_game,
    check_positivity,
)
from shapleypy.generators import (
    ReturnType,
    k_additive_game_generator,
    k_game_generator,
    positive_game_generator,
    random_game_generator,
)


def test_random_game_generator() -> None:
    # This also tests _generate_random function
    game = random_game_generator(10)
    assert all(0 <= value <= 1 for value in game._values[1:])
    game = random_game_generator(
        10, return_type=ReturnType.INTEGER, lower_bound=0, upper_bound=10
    )
    assert all(0 <= value <= 10 for value in game._values[1:])
    assert all(value.is_integer() for value in game._values[1:])
    game = random_game_generator(10, lower_bound=0, upper_bound=10)
    assert all(0 <= value <= 10 for value in game._values[1:])
    assert all(not value.is_integer() for value in game._values[1:])
    with pytest.raises(ValueError):
        random_game_generator(10, lower_bound=10, upper_bound=0)


def test_positive_game_generator() -> None:
    game = positive_game_generator(5)
    assert all(not value.is_integer() for value in game._values[1:])
    assert check_positivity(game)
    game = positive_game_generator(
        5, return_type=ReturnType.INTEGER, lower_bound=0, upper_bound=10
    )
    assert all(value.is_integer() for value in game._values[1:])
    assert check_positivity(game)
    with pytest.raises(ValueError):
        positive_game_generator(5, lower_bound=-1)


@pytest.mark.skipif(
    sys.platform != "linux", reason="convex_game_generator is not available"
)
def test_convex_game_generator() -> None:
    # I was unable to properly set c++ flags to compile the extension for
    # MacOS so skip this test if the extension is not available
    from shapleypy.generators import convex_game_generator

    game = convex_game_generator(5)
    assert check_convexity(game)


def test_k_game_generator() -> None:
    game = k_game_generator(5, k=3)
    assert check_k_game(game, 3)


def test_k_additive_game_generator() -> None:
    game = k_additive_game_generator(5, k=3)
    assert check_k_additivity(game, 3)
