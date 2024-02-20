from __future__ import annotations

import csv
import json

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.constants import CSV_SEPARATOR_ERROR
from shapleypy.game import Game


def _prepare_game_dict(game: Game) -> dict:
    return {
        "n": game.number_of_players,
        "values": {
            str(list(coalition.get_players)): value
            for coalition, value in game.get_values(
                Coalition.all_coalitions(game.number_of_players)
            )
            if not np.isnan(value)
        },
    }


def save_game_to_json(game: Game, filename: str) -> None:
    prepared_game = _prepare_game_dict(game)

    with open(filename, "w") as file:
        json.dump(prepared_game, file)


def save_game_to_csv(
    game: Game,
    filename: str,
    csv_separator: str = ":",
    coalition_separator: str = ",",
) -> None:
    if csv_separator == coalition_separator:
        raise ValueError(CSV_SEPARATOR_ERROR)

    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=csv_separator)
        writer.writerow(["n", game.number_of_players])
        for coalition, value in game.get_values(
            Coalition.all_coalitions(game.number_of_players)
        ):
            if not np.isnan(value):
                writer.writerow(
                    [
                        coalition_separator.join(
                            map(str, coalition.get_players)
                        ),
                        value,
                    ]
                )
