# ruff: noqa: N806, B008
from __future__ import annotations

from enum import Enum

import numpy as np

from shapleypy.classes_checkers import check_convexity
from shapleypy.constants import (
    CONVEX_GAME_GENERATOR_ERROR,
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


# ruff: noqa: ARG001
def convex_game_generator(
    number_of_players: int,
    generator: np.random.Generator = np.random.default_rng(),
    return_type: ReturnType = ReturnType.FLOAT,
    lower_bound: int = 0,
    upper_bound: int = 1,
) -> Game:
    """
    Generates a random convex game.

    WARNING: This function is not optimal and will be changed in the future.
             Even for relatively small number_of_players it takes quite a while
             to compute. This function requires the 'pyfmtools' package to be
             installed and is available only on Linux for time being.

    Note: The only parameter that is used is the number_of_players. The others
          are there so all the generators have the same arguments.

    Args:
        number_of_players (int): The number of players in the game.
        generator (np.random.Generator): Random generator to use.
        return_type (ReturnType): Type of the return value.
            Either FLOAT or INTEGER.
        lower_bound (int): Lower bound for the random number (included).
        upper_bound (int): Upper bound for the random number (excluded).

    Returns:
        Game: The generated convex game.
    """
    try:
        import pyfmtools as fmp  # type: ignore[import-untyped]
    except ModuleNotFoundError:
        raise ImportError(CONVEX_GAME_GENERATOR_ERROR) from None

    env = fmp.fm_init(number_of_players)

    game = Game(number_of_players)
    while True:
        _, values = fmp.generate_fmconvex_tsort(
            1, number_of_players, number_of_players - 1, 1000, 1, 1000, env
        )
        converted_values = fmp.ConvertCard2Bit(values, env)
        if fmp.IsMeasureSupermodular(converted_values, env):
            game.set_values(list(zip(game.all_coalitions, converted_values)))
            if check_convexity(game):
                break

    fmp.fm_free(env)

    return game


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
