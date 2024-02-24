from __future__ import annotations

import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.loaders import (
    load_game_from_csv,
    load_game_from_json,
)
from shapleypy.savers import (
    save_game_to_csv,
    save_game_to_json,
)


@pytest.fixture
def basic_values_for_game_of_three_coalition_form() -> (
    list[tuple[Coalition, float]]
):
    return [
        (Coalition.from_players([0]), 1.0),
        (Coalition.from_players([1]), 2.0),
        (Coalition.from_players([0, 1]), 3.0),
        (Coalition.from_players([2]), 4.0),
        (Coalition.from_players([0, 2]), 5.0),
        (Coalition.from_players([1, 2]), 6.0),
        (Coalition.from_players([0, 1, 2]), 7.0),
    ]


def test_save_and_load_game_to_json_with_values(  # type: ignore
    basic_values_for_game_of_three_coalition_form: list[
        tuple[Coalition, float]
    ],
    tmpdir,
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    file = tmpdir.join("game.json")
    save_game_to_json(game, str(file))
    loaded_game = load_game_from_json(str(file))
    assert game == loaded_game


def test_save_and_load_game_to_json_empty(tmpdir) -> None:  # type: ignore
    game = Game(3)
    file = tmpdir.join("game.json")
    save_game_to_json(game, str(file))
    loaded_game = load_game_from_json(str(file))
    assert game == loaded_game


def test_save_and_load_game_to_csv_with_values(  # type: ignore
    basic_values_for_game_of_three_coalition_form: list[
        tuple[Coalition, float]
    ],
    tmpdir,
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    file = tmpdir.join("game.csv")
    save_game_to_csv(game, str(file))
    loaded_game = load_game_from_csv(str(file))
    assert game == loaded_game


def test_save_and_load_game_to_csv_empty(tmpdir) -> None:  # type: ignore
    game = Game(3)
    file = tmpdir.join("game.csv")
    save_game_to_csv(game, str(file))
    loaded_game = load_game_from_csv(str(file))
    assert game == loaded_game
