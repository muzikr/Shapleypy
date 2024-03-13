from __future__ import annotations

import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.normalization import (
    standart_normalization,
    zero_one_normalization,
)


@pytest.fixture
def basic_values_for_game_of_three_coalition_form() -> (
    list[tuple[Coalition, float]]
):
    return [
        (Coalition.from_players([0]), 1.0),
        (Coalition.from_players([1]), 1.0),
        (Coalition.from_players([0, 1]), 4.0),
        (Coalition.from_players([2]), 1.0),
        (Coalition.from_players([0, 2]), 4.0),
        (Coalition.from_players([1, 2]), 4.0),
        (Coalition.from_players([0, 1, 2]), 9.0),
    ]


def test_standart_normalization(
    basic_values_for_game_of_three_coalition_form: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    standart_normalization(game)
    assert all(
        game.get_value(coalition)
        == value / basic_values_for_game_of_three_coalition_form[-1][1]
        for coalition, value in basic_values_for_game_of_three_coalition_form
    )


def test_zero_one_normalization(
    basic_values_for_game_of_three_coalition_form: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    zero_one_normalization(game)
    assert all(
        x == y
        for x, y in zip(
            list(game._values[1:]), [0.0, 0.0, 2 / 6, 0.0, 2 / 6, 2 / 6, 1.0]
        )
    )
