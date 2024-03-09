from __future__ import annotations

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.game import Game


def standart_normalization(game: Game) -> None:
    value_of_grand_coalition = game.get_value(
        Coalition(2**game.number_of_players - 1)
    )
    game._values /= value_of_grand_coalition
