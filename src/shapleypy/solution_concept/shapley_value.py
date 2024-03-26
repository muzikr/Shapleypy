from __future__ import annotations

from collections.abc import Iterable
from math import factorial
from typing import Any

import numpy as np

from shapleypy._typing import Player, Value, ValueInput
from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.solution_concept._default_value import set_default_value


def _get_weights(game: Game) -> np.ndarray[Any, np.dtype[Value]]:
    """
    Get the weights for the Shapley value calculation.

    Args:
        game (Game): The game for which to calculate the weights.

    Returns:
        np.ndarray: The weights for the Shapley value calculation (for each size
            of coalition).
    """
    n = game.number_of_players
    weights = np.array([factorial(i) * factorial(n - i - 1) for i in range(n)])
    return weights


def _shapley_value_of_player(
    game: Game,
    player: Player,
    weights: np.ndarray[Any, np.dtype[Value]],
    n_fac: int,
    default_value: ValueInput | None,
) -> Value:
    """
    Compute the Shapley value of a player in a game (weights and factorial are
    precomputed).

    Args:
        game (Game): The game for which to compute the Shapley value.
        player (Player): The player for which to compute the Shapley value.
        weights (np.ndarray): The weights for the Shapley value calculation.
        n_fac (int): The factorial of the number of players.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Value: The Shapley value of the player.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
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
    game: Game, player: Player, default_value: ValueInput | None = None
) -> Value:
    """
    Compute the Shapley value of a player in a game.

    Args:
        game (Game): The game for which to compute the Shapley value.
        player (Player): The player for which to compute the Shapley value.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Value: The Shapley value of the player.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    weights = _get_weights(game)
    n_fac = factorial(game.number_of_players)
    return _shapley_value_of_player(game, player, weights, n_fac, default_value)


def shapley_value_of_game(
    game: Game, default_value: ValueInput | None = None
) -> Iterable[Value]:
    """
    Compute the Shapley value of all players in a game.

    Args:
        game (Game): The game for which to compute the Shapley value.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Iterable[Value]: The Shapley value of all players in the game (payoff
            vector).

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    weights = _get_weights(game)
    n_fac = factorial(game.number_of_players)
    for player in range(game.number_of_players):
        yield _shapley_value_of_player(
            game, player, weights, n_fac, default_value
        )


def shapley(
    game: Game,
    player: Player | None = None,
    default_value: ValueInput | None = None,
) -> Value | Iterable[Value]:
    """
    Compute the Shapley value of a player in a game or the Shapley values of
    all players in a game.

    Args:
        game (Game): The game for which to compute the Shapley value(s).
        player (Player | None): The player for which to compute the Shapley
            value (if None Shapley values of all players will be computed).
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Value | Iterable[Value]: The Shapley value of the player or the Shapley
            values of all players in the game (payoff vector).

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    if player is not None:
        return shapley_value_of_player(game, player, default_value)
    return shapley_value_of_game(game, default_value)
