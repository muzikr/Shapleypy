from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.protocols import Player, Value
from shapleypy.solution_concept._default_value import set_default_value


def _banzhaf_value_of_player(
    game: Game,
    player: Player,
    factor: int,
    default_value: Value | float | None,
) -> Value:
    coalitions_without_player = np.array(
        list(
            {
                coalition - player
                for coalition in Coalition.all_coalitions(
                    game.number_of_players
                )
            }
        )
    )
    coalitions_with_player = np.array(
        [coalition + player for coalition in coalitions_without_player]
    )

    values_of_coalitions_without_player = np.array(
        [value for _, value in game.get_values(coalitions_without_player)]
    )
    values_of_coalitions_with_player = np.array(
        [value for _, value in game.get_values(coalitions_with_player)]
    )

    values_of_coalitions_without_player = set_default_value(
        values_of_coalitions_without_player, default_value
    )
    values_of_coalitions_with_player = set_default_value(
        values_of_coalitions_with_player, default_value
    )

    marginal_contributions = (
        values_of_coalitions_with_player - values_of_coalitions_without_player
    )

    return np.sum(marginal_contributions) / factor


def banzhaf_value_of_player(
    game: Game, player: Player, default_value: Value | float | None = None
) -> Value:
    factor = 2 ** (game.number_of_players - 1)
    return _banzhaf_value_of_player(game, player, factor, default_value)


def banzhaf_value_of_game(
    game: Game, default_value: Value | float | None = None
) -> Iterable[Value]:
    factor = 2 ** (game.number_of_players - 1)
    for player in range(game.number_of_players):
        yield _banzhaf_value_of_player(game, player, factor, default_value)


def banzhaf(
    game: Game,
    player: Player | None = None,
    default_value: Value | float | None = None,
) -> Value | Iterable[Value]:
    if player is not None:
        return banzhaf_value_of_player(game, player, default_value)
    return banzhaf_value_of_game(game, default_value)
