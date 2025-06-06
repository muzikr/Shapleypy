# ruff: noqa: N806, B008
from __future__ import annotations

from enum import Enum

import numpy as np

from shapleypy.constants import (
    K_GAMES_PARAMETER,
    POSITIVE_GAME_GENERATOR_LOWER_BOUND_ERROR,
)
from shapleypy.game import Game


class ReturnType(Enum):
    FLOAT = 1
    INTEGER = 2


def _generate_random(
    generator: np.random.Generator,
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
) -> float:
    """
    Combination of random generators to generate floats or integers between
    given bounds.

    Args:
        generator (np.random.Generator): Random generator to use.
        return_type (ReturnType): Type of the return value.
            Either FLOAT or INTEGER.
        lower_bound (int): Lower bound for the random number (included).
        upper_bound (int): Upper bound for the random number (excluded).

    Returns:
        float: Random number between lower_bound and upper_bound.
    """
    return (
        generator.integers(lower_bound, upper_bound)
        if return_type == ReturnType.INTEGER
        else generator.integers(lower_bound, upper_bound) + generator.random()
    )


def _compute_game_from_unanimity_game(unanimity_game: Game) -> Game:
    """
    Computes the game from the given unanimity game.

    Args:
        unanimity_game (Game): The unanimity game to compute the game from.

    Returns:
        Game: The computed game.
    """
    game = Game(unanimity_game.number_of_players)
    for S in game.all_coalitions:
        v_S = sum(unanimity_game.get_value(T) for T in S.all_subcoalitions())
        game.set_value(S, v_S)
    return game


def random_game_generator(
    number_of_players: int,
    generator: np.random.Generator = np.random.default_rng(),
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
) -> Game:
    """
    Generates a random game (=each coalition value is random) with values
    between lower_bound and upper_bound.

    Args:
        number_of_players (int): The number of players in the game.
        generator (np.random.Generator): Random generator to use.
        return_type (ReturnType): Type of the return value.
            Either FLOAT or INTEGER.
        lower_bound (int): Lower bound for the random number (included).
        upper_bound (int): Upper bound for the random number (excluded).

    Returns:
        Game: The generated game.
    """
    game = Game(number_of_players)

    for S in game.all_coalitions:
        random_number = _generate_random(
            generator, return_type, lower_bound, upper_bound
        )
        game.set_value(S, random_number)

    return game


def positive_game_generator(
    number_of_players: int,
    generator: np.random.Generator = np.random.default_rng(),
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
) -> Game:
    """
    Generates a random positive game.

    Args:
        number_of_players (int): The number of players in the game.
        generator (np.random.Generator): Random generator to use.
        return_type (ReturnType): Type of the return value.
            Either FLOAT or INTEGER.
        lower_bound (int): Lower bound for the random number (included).
        upper_bound (int): Upper bound for the random number (excluded).

    Returns:
        Game: The generated positive game.
    """
    if lower_bound < 0:
        raise ValueError(POSITIVE_GAME_GENERATOR_LOWER_BOUND_ERROR)

    # Generate m^v(S) for each S in 2^N
    m_v_game = random_game_generator(
        number_of_players,
        generator,
        return_type=return_type,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
    )

    return _compute_game_from_unanimity_game(m_v_game)


def k_game_generator(
    number_of_players: int,
    generator: np.random.Generator = np.random.default_rng(),
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
    k: int = 1,
) -> Game:
    """
    Generates a random k-game.

    Args:
        number_of_players (int): The number of players in the game.
        generator (np.random.Generator): Random generator to use.
        return_type (ReturnType): Type of the return value.
            Either FLOAT or INTEGER.
        lower_bound (int): Lower bound for the random number (included).
        upper_bound (int): Upper bound for the random number (excluded).
        k (int): The parameter k for the k-game.

    Returns:
        Game: The generated k-game.
    """
    if lower_bound < 0:
        raise ValueError(POSITIVE_GAME_GENERATOR_LOWER_BOUND_ERROR)

    if not 0 < k <= number_of_players:
        raise ValueError(K_GAMES_PARAMETER)

    # Generate m^v(S) for each S in 2^N
    m_v_game = Game(number_of_players)

    for S in m_v_game.all_coalitions:
        if len(S) == k:
            random_number = _generate_random(
                generator, return_type, lower_bound, upper_bound
            )
        else:
            random_number = 0
        m_v_game.set_value(S, random_number)

    return _compute_game_from_unanimity_game(m_v_game)


def k_additive_game_generator(
    number_of_players: int,
    generator: np.random.Generator = np.random.default_rng(),
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
    k: int = 1,
) -> Game:
    """
    Generates a random k-additive game.

    Args:
        number_of_players (int): The number of players in the game.
        generator (np.random.Generator): Random generator to use.
        return_type (ReturnType): Type of the return value.
            Either FLOAT or INTEGER.
        lower_bound (int): Lower bound for the random number (included).
        upper_bound (int): Upper bound for the random number (excluded).
        k (int): The parameter k for the k-additive game.

    Returns:
        Game: The generated k-additive game.
    """
    if lower_bound < 0:
        raise ValueError(POSITIVE_GAME_GENERATOR_LOWER_BOUND_ERROR)

    if not 0 < k <= number_of_players:
        raise ValueError(K_GAMES_PARAMETER)

    # Generate m^v(S) for each S in 2^N
    m_v_game = Game(number_of_players)

    for S in m_v_game.all_coalitions:
        if len(S) <= k:
            random_number = _generate_random(
                generator, return_type, lower_bound, upper_bound
            )
        else:
            random_number = 0
        m_v_game.set_value(S, random_number)

    return _compute_game_from_unanimity_game(m_v_game)
