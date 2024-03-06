# ruff: noqa: N806
from __future__ import annotations

from shapleypy.coalition import (
    EMPTY_COALITION,
    Coalition,
    all_one_player_missing_subcoalitions,
)
from shapleypy.game import Game


def check_monotonicity(game: Game) -> bool:
    """
    Check if the game is monotone.
    """
    for S in game.all_coalitions:
        # Check the values of all subcoalitions of size |S| - 1
        for S_minus_one in all_one_player_missing_subcoalitions(S):
            if game.get_value(S) < game.get_value(S_minus_one):
                return False
    return True


def check_weakly_superadditivity(game: Game) -> bool:
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    for i in range(game.number_of_players):
        for S in (grand_coalition - i).all_subcoalitions():
            if game.get_value(S) + game.get_value([i]) > game.get_value(S + i):
                return False
    return True


def check_superadditivity(game: Game) -> bool:
    for T in game.all_coalitions:
        for S in filter(
            lambda s: T * s == EMPTY_COALITION, game.all_coalitions
        ):
            if game.get_value(T) + game.get_value(S) > game.get_value(T + S):
                return False
    return True


def check_convexity(game: Game) -> bool:
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    for i in range(game.number_of_players):
        for T in (grand_coalition - i).all_subcoalitions():
            for S in T.all_subcoalitions():
                if game.get_value(S + i) - game.get_value(S) > game.get_value(
                    T + i
                ) - game.get_value(T):
                    return False
    return True


def check_supermodularity(game: Game) -> bool:
    return check_convexity(game)
