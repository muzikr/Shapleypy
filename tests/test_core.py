from __future__ import annotations

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.solution_concept.core import _get_payoff, solution_in_core


def test_get_payoff() -> None:
    assert _get_payoff(Coalition.from_players([0]), np.array([1.0, 2.0])) == 1.0
    assert _get_payoff(Coalition.from_players([1]), np.array([1.0, 2.0])) == 2.0
    assert (
        _get_payoff(Coalition.from_players([0, 1]), np.array([1.0, 2.0])) == 3.0
    )


def test_solution_in_core() -> None:
    game = Game(2)
    game.set_value(Coalition.from_players([0]), 0.0)
    game.set_value(Coalition.from_players([1]), 0.0)
    game.set_value(Coalition.from_players([0, 1]), 1.0)
    assert solution_in_core(game, [0.5, 0.5])
    assert not solution_in_core(game, [0.5, 0.4])
    assert not solution_in_core(game, [1.0, 5.0])
