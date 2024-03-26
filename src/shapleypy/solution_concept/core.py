from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy.constants import CORE_POINT_ERROR, CORE_WINDOWS_ERROR

try:
    import ppl  # type: ignore[import-untyped]
except ModuleNotFoundError:
    raise ImportError(CORE_WINDOWS_ERROR) from None

from shapleypy._typing import Value, ValueInput
from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.solution_concept._default_value import set_default_value


def _get_payoff(
    coalition: Coalition,
    payoff_vector: Iterable[ValueInput],
) -> Value:
    """
    Get the payoff of a coalition in a game (sum of payoffs of singletons in
    given coalition).

    Args:
        coalition (Coalition): The coalition for which to get the payoff.
        payoff_vector (Iterable[ValueInput]): The vector of payoffs.

    Returns:
        Value: The payoff of the coalition.
    """
    return np.sum(np.array(payoff_vector)[list(coalition.get_players)])


def _get_polyhedron_of_game(
    game: Game, default_value: ValueInput | None = None
) -> ppl.Polyhedron:
    """
    Get the polyhedron of a game.

    Args:
        game (Game): The game for which to get the polyhedron.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        ppl.Polyhedron: The polyhedron of the game.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    constrain_system = ppl.Constraint_System()

    # Just preimputations
    numerator, denominator = set_default_value(
        np.array(
            [game.get_value(Coalition.grand_coalition(game.number_of_players))]
        ),
        default_value,
    )[0].as_integer_ratio()
    constrain_system.insert(
        ppl.Linear_Expression(
            {
                player: 1 * denominator
                for player in range(game.number_of_players)
            },
            0,
        )
        == numerator
    )

    for coalition in game.all_coalitions:
        numerator, denominator = set_default_value(
            np.array([game.get_value(coalition)]), default_value
        )[0].as_integer_ratio()
        constrain_system.insert(
            ppl.Linear_Expression(
                {player: 1 * denominator for player in coalition.get_players}, 0
            )
            >= numerator
        )

    return ppl.C_Polyhedron(constrain_system)


def _convert_point_to_vector(point: ppl.Generator) -> tuple[float]:
    """
    Convert a point to a vector.

    Args:
        point (ppl.Generator): The point to convert.

    Returns:
        tuple: The vector of the point (might be higher dimension).

    Raises:
        TypeError: If the point is not a point. Not sure if this is possible. If
            it is, please contact the developer.
    """
    if not point.is_point():
        raise TypeError(CORE_POINT_ERROR)
    divisor = point.divisor()
    return tuple(
        float(coefficient) / divisor for coefficient in point.coefficients()
    )


def solution_in_core(
    game: Game,
    payoff_vector: Iterable[ValueInput],
    default_value: ValueInput | None = None,
) -> bool:
    """
    Check if a solution is in the core of a game.

    Args:
        game (Game): The game for which to check the solution.
        payoff_vector (Iterable[ValueInput]): The vector of payoffs.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        bool: True if the solution is in the core, False otherwise.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    return _get_payoff(
        Coalition.grand_coalition(game.number_of_players),
        np.array(payoff_vector),
    ) == game.get_value(
        Coalition.grand_coalition(game.number_of_players)
    ) and all(
        _get_payoff(coalition, payoff_vector)
        >= set_default_value(
            np.array([game.get_value(coalition)]), default_value
        )[0]
        for coalition in game.all_coalitions
    )


def is_empty(game: Game, default_value: ValueInput | None = None) -> bool:
    """
    Check if the core of a game is empty.

    Args:
        game (Game): The game for which to check the core.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        bool: True if the core is empty, False otherwise.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    return _get_polyhedron_of_game(game, default_value).is_empty()


def get_vertices(
    game: Game, default_value: ValueInput | None = None
) -> Iterable[tuple[float]]:
    """
    Get the vertices of the core of a game.

    Args:
        game (Game): The game for which to get the vertices.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Yields:
        tuple: The vertices of the core of the game.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
        TypeError: If the point is not a point. Not sure if this is possible. If
            it is, please contact the developer
    """
    yield from (
        _convert_point_to_vector(vertex)
        for vertex in _get_polyhedron_of_game(
            game, default_value
        ).minimized_generators()
    )


def contains_integer_point(
    game: Game, default_value: ValueInput | None = None
) -> bool:
    """
    Check if the core of a game contains an integer solution.

    Args:
        game (Game): The game for which to check the core.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        bool: True if the core contains an integer solution, False otherwise.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    return _get_polyhedron_of_game(game, default_value).contains_integer_point()


def get_core_polyhedron(
    game: Game, default_value: ValueInput | None = None
) -> ppl.Polyhedron:
    """
    Get the polyhedron of the core of a game. Check pplpy documentation
    for more information.

    Args:
        game (Game): The game for which to get the polyhedron.
        default_value (ValueInput | None): The default value to set to the
            missing values (if None DEFAULT_VALUE from constants will be used).

    Returns:
        ppl.Polyhedron: The polyhedron of the core of the game.

    Raises:
        RuntimeWarning: If the default value is used and was not set by user.
    """
    return _get_polyhedron_of_game(game, default_value)
