from __future__ import annotations

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.game import Game


def standart_normalization(game: Game) -> None:
    value_of_grand_coalition = game.get_value(
        Coalition(2**game.number_of_players - 1)
    )
    game._values /= value_of_grand_coalition


def zero_one_normalization(game: Game) -> None:
    value_of_singletons = np.array(
        [
            game.get_value(Coalition.from_players([i]))
            for i in range(game.number_of_players)
        ]
    )
    for coalition in game.all_coalitions:
        game.set_value(
            coalition,
            game.get_value(coalition)
            - np.sum(value_of_singletons[list(coalition.get_players)]),
        )
    standart_normalization(game)
