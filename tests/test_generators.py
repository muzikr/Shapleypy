from __future__ import annotations

import pytest

from shapleypy.generators import ReturnType, random_game_generator


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
