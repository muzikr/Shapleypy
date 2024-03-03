from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import ppl  # type: ignore

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.protocols import Value
from shapleypy.solution_concept._default_value import set_default_value


def _get_payoff(
    coalition: Coalition,
    payoff_vector: Iterable[Value | float],
) -> Value:
    """
    Get the payoff of a coalition in a game.
    """
    return np.sum(np.array(payoff_vector)[list(coalition.get_players)])


def _get_polyhedron_of_game(game: Game) -> ppl.Polyhedron:
    """
    Get the polyhedron of a game.
    """
    constrain_system = ppl.Constraint_System()

    # Just preimputations
    numerator, denominator = game.get_value(
        Coalition.grand_coalition(game.number_of_players)
    ).as_integer_ratio()
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

    for coalition in Coalition.all_coalitions(game.number_of_players):
        numerator, denominator = game.get_value(coalition).as_integer_ratio()
        constrain_system.insert(
            ppl.Linear_Expression(
                {player: 1 * denominator for player in coalition.get_players}, 0
            )
            >= numerator
        )

    return ppl.C_Polyhedron(constrain_system)


def solution_in_core(
    game: Game,
    payoff_vector: Iterable[Value | float],
    default_value: Value | float | None = None,
) -> bool:
    """
    Check if a solution is in the core of a game.
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
        for coalition in Coalition.all_coalitions(game.number_of_players)
    )
