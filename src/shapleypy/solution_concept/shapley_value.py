from __future__ import annotations

from collections.abc import Iterable
from math import factorial
from typing import Any

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.protocols import Player, Value
from shapleypy.solution_concept._default_value import set_default_value


def _get_weights(game: Game) -> np.ndarray[Any, np.dtype[Value]]:
    n = game.number_of_players
    weights = np.array([factorial(i) * factorial(n - i - 1) for i in range(n)])
    return weights


def _shapley_value_of_player(
    game: Game,
    player: Player,
    weights: np.ndarray[Any, np.dtype[Value]],
    n_fac: int,
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

    filtered_weights = weights[list(map(len, coalitions_without_player))]

    return np.sum(marginal_contributions * filtered_weights) / n_fac


def shapley_value_of_player(
    game: Game, player: Player, default_value: Value | float | None = None
) -> Value:
    weights = _get_weights(game)
    n_fac = factorial(game.number_of_players)
    return _shapley_value_of_player(game, player, weights, n_fac, default_value)


def shapley_value_of_game(
    game: Game, default_value: Value | float | None = None
) -> Iterable[Value]:
    weights = _get_weights(game)
    n_fac = factorial(game.number_of_players)
    for player in range(game.number_of_players):
        yield _shapley_value_of_player(
            game, player, weights, n_fac, default_value
        )


def shapley(
    game: Game,
    player: Player | None = None,
    default_value: Value | float | None = None,
) -> Value | Iterable[Value]:
    if player is not None:
        return shapley_value_of_player(game, player, default_value)
    return shapley_value_of_game(game, default_value)