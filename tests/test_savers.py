from __future__ import annotations

import csv
import json

import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.savers import (
    _prepare_game_dict,
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


@pytest.fixture
def output_dict() -> dict:
    return {
        "n": 3,
        "values": {
            "[0]": 1.0,
            "[1]": 2.0,
            "[0, 1]": 3.0,
            "[2]": 4.0,
            "[0, 2]": 5.0,
            "[1, 2]": 6.0,
            "[0, 1, 2]": 7.0,
        },
    }


def test_prepare_game_dict(
    basic_values_for_game_of_three_coalition_form: list[
        tuple[Coalition, float]
    ],
    output_dict: dict,
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    assert _prepare_game_dict(game) == output_dict


def test_save_game_to_json(  # type: ignore
    basic_values_for_game_of_three_coalition_form: list[
        tuple[Coalition, float]
    ],
    output_dict: dict,
    tmpdir,
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    file = tmpdir.join("game.json")
    save_game_to_json(game, str(file))
    assert json.load(file) == output_dict


def test_save_game_to_csv(  # type: ignore
    basic_values_for_game_of_three_coalition_form: list[
        tuple[Coalition, float]
    ],
    tmpdir,
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    file = tmpdir.join("game.csv")
    save_game_to_csv(game, str(file))
    i = 0
    with open(file) as f:
        reader = csv.reader(f, delimiter=":")
        assert next(reader) == ["n", "3"]
        for row in reader:
            if row:
                coalition, value = (
                    basic_values_for_game_of_three_coalition_form[i]
                )
                i += 1
                read_coalition = [int(x) for x in row[0].split(",")]
                read_value = float(row[1])
                assert [read_coalition, read_value] == [
                    list(coalition.get_players),
                    value,
                ]
    # Check if all values were read
    assert i == len(basic_values_for_game_of_three_coalition_form)
