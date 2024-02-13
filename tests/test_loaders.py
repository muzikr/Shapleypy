import numpy as np
import pytest

from shapleypy.game import Game
from shapleypy.loaders import load_game_from_csv, load_game_from_json


@pytest.fixture
def basic_game_of_three() -> Game:
    game = Game(3)
    game._values = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    return game


@pytest.fixture
def partial_game_of_three() -> Game:
    game = Game(3)
    game._values = np.array([0.0, 1.0, 2.0, np.nan, np.nan, np.nan, 6.0, 7.0])
    return game


# region load_game_from_json


def test_json_input(basic_game_of_three: Game) -> None:
    loaded_game = load_game_from_json(
        "tests/input_data/json/basic_game_of_three.json"
    )
    assert loaded_game.number_of_players == 3
    assert np.array_equal(loaded_game._values, basic_game_of_three._values)
    assert basic_game_of_three == loaded_game


def test_json_missing_number_of_players() -> None:
    with pytest.raises(ValueError):
        load_game_from_json("tests/input_data/json/missing_n.json")


def test_json_missing_values() -> None:
    game = load_game_from_json("tests/input_data/json/missing_values.json")
    assert game.number_of_players == 3
    assert game == Game(3)


def test_json_empty_values() -> None:
    game = load_game_from_json("tests/input_data/json/empty_values.json")
    assert game.number_of_players == 3
    assert game == Game(3)


def test_json_partial_values(partial_game_of_three: Game) -> None:
    loaded_game = load_game_from_json(
        "tests/input_data/json/partial_values.json"
    )
    assert loaded_game.number_of_players == 3
    assert loaded_game == partial_game_of_three


# endregion

# region load_game_from_csv


def test_csv_input(basic_game_of_three: Game) -> None:
    loaded_game = load_game_from_csv(
        "tests/input_data/csv/basic_game_of_three.csv"
    )
    assert loaded_game.number_of_players == 3
    assert basic_game_of_three == loaded_game


def test_csv_missing_number_of_players() -> None:
    with pytest.raises(ValueError):
        load_game_from_csv("tests/input_data/csv/missing_n.csv")


def test_csv_missing_values() -> None:
    game = load_game_from_csv("tests/input_data/csv/missing_values.csv")
    assert game.number_of_players == 3
    assert game == Game(3)


def test_csv_partial_values(partial_game_of_three: Game) -> None:
    loaded_game = load_game_from_csv("tests/input_data/csv/partial_values.csv")
    assert loaded_game.number_of_players == 3
    assert loaded_game == partial_game_of_three


def test_csv_same_separators() -> None:
    with pytest.raises(ValueError):
        load_game_from_csv(
            "tests/input_data/csv/basic_game_of_three.csv",
            csv_separator=",",
            coalition_separator=",",
        )


# endregion
