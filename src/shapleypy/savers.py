from __future__ import annotations

import json

import numpy as np

from shapleypy.coalition import Coalition
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
