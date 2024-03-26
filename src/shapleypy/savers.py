from __future__ import annotations

import csv
import json

import numpy as np

from shapleypy.constants import CSV_SEPARATOR_ERROR
from shapleypy.game import Game


def _prepare_game_dict(game: Game) -> dict:
    """
    Prepares the game to be saved to a JSON file.

    Args:
        game (Game): The game to prepare.

    Returns:
        dict: The prepared game.
    """
    return {
        "n": game.number_of_players,
        "values": {
            str(list(coalition.get_players)): value
            for coalition, value in game.get_values(game.all_coalitions)
            if not np.isnan(value)
        },
    }


def save_game_to_json(game: Game, filename: str) -> None:
    """
    Saves the game to a JSON file.

    Args:
        game (Game): The game to save.
        filename (str): The path to the JSON file.

    Returns:
        None
    """
    prepared_game = _prepare_game_dict(game)

    with open(filename, "w") as file:
        json.dump(prepared_game, file)


def save_game_to_csv(
    game: Game,
    filename: str,
    csv_separator: str = ":",
    coalition_separator: str = ",",
) -> None:
    """
    Saves the game to a CSV file.

    Args:
        game (Game): The game to save.
        filename (str): The path to the CSV file.
        csv_separator (str): The separator to use in the CSV file (default is
            compatible with loaders).
        coalition_separator (str): The separator to use for the coalitions
            (default is compatible with loaders).

    Returns:
        None
    """
    if csv_separator == coalition_separator:
        raise ValueError(CSV_SEPARATOR_ERROR)

    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=csv_separator)
        writer.writerow(["n", game.number_of_players])
        for coalition, value in game.get_values(game.all_coalitions):
            if not np.isnan(value):
                writer.writerow(
                    [
                        coalition_separator.join(
                            map(str, coalition.get_players)
                        ),
                        value,
                    ]
                )
