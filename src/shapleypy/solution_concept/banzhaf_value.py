from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy._typing import Player, Value, ValueInput
from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.solution_concept._default_value import set_default_value


def _banzhaf_value_of_player(
    game: Game,
    player: Player,
    factor: int,
    default_value: ValueInput | None,
) -> Value:
    """
    Compute the Banzhaf value of a player in a game (precomputed factor).

    Args:
        game (Game): The game for which to compute the Banzhaf value.
        player (Player): The player for which to compute the Banzhaf value.
        factor (int): The factor to divide the Banzhaf value by (since it is n!
            it takes time to compute so reusing it).
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Value: The Banzhaf value of the player.

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

    return np.sum(marginal_contributions) / factor


def banzhaf_value_of_player(
    game: Game, player: Player, default_value: ValueInput | None = None
) -> Value:
    """
    Compute the Banzhaf value of a player in a game.

    Args:
        game (Game): The game for which to compute the Banzhaf value.
        player (Player): The player for which to compute the Banzhaf value.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Value: The Banzhaf value of the player.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    factor = 2 ** (game.number_of_players - 1)
    return _banzhaf_value_of_player(game, player, factor, default_value)


def banzhaf_value_of_game(
    game: Game, default_value: ValueInput | None = None
) -> Iterable[Value]:
    """
    Compute the Banzhaf values of all players in a game.

    Args:
        game (Game): The game for which to compute the Banzhaf values.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Iterable[Value]: The Banzhaf values of all players (payoff vector).

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    factor = 2 ** (game.number_of_players - 1)
    for player in range(game.number_of_players):
        yield _banzhaf_value_of_player(game, player, factor, default_value)


def banzhaf(
    game: Game,
    player: Player | None = None,
    default_value: ValueInput | None = None,
) -> Value | Iterable[Value]:
    """
    Compute the Banzhaf value of a player in a game or the Banzhaf values of
    all players in a game.

    Args:
        game (Game): The game for which to compute the Banzhaf value(s).
        player (Player | None): The player for which to compute the Banzhaf
            value (if None Banzhaf values of all players will be computed).
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        Value | Iterable[Value]: The Banzhaf value of the player or the Banzhaf
            values of all players in the game.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    if player is not None:
        return banzhaf_value_of_player(game, player, default_value)
    return banzhaf_value_of_game(game, default_value)
