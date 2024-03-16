# ruff: noqa: N806, B008
from __future__ import annotations

from enum import Enum

import numpy as np

from shapleypy.classes_checkers import check_convexity
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
    generator must implement random (return floats between 0 and 1)
    and integers (returns integer between lower and uper bound) methods.
    """
    return (
        generator.integers(lower_bound, upper_bound)
        if return_type == ReturnType.INTEGER
        else generator.integers(lower_bound, upper_bound) + generator.random()
    )


def _compute_game_from_unanimity_game(unanimity_game: Game) -> Game:
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
    r"""
    generator will be used to generate m^v(S) for all S in 2^N and the v(S) is
    computed as \sum_{T \subseteq S} m^v(T)
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
    import pyfmtools as fmp  # type: ignore[import-untyped]

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
