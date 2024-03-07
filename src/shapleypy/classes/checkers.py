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
        value_of_S = game.get_value(S)
        for S_minus_one in all_one_player_missing_subcoalitions(S):
            if value_of_S < game.get_value(S_minus_one):
                return False
    return True


def check_weakly_superadditivity(game: Game) -> bool:
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    for i in range(game.number_of_players):
        value_of_i = game.get_value([i])
        for S in (grand_coalition - i).all_subcoalitions():
            if game.get_value(S) + value_of_i > game.get_value(S + i):
                return False
    return True


def check_superadditivity(game: Game) -> bool:
    for T in game.all_coalitions:
        value_of_T = game.get_value(T)
        for S in filter(
            lambda s: T * s == EMPTY_COALITION, game.all_coalitions
        ):
            if value_of_T + game.get_value(S) > game.get_value(T + S):
                return False
    return True


def check_convexity(game: Game) -> bool:
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    # We can use just i < j, because it the condition is symmetric
    # (if we exchange i and j, we get the same condition)
    for i in range(game.number_of_players - 1):
        grand_coalition_without_i = grand_coalition - i
        for j in range(i + 1, game.number_of_players):
            for S in (grand_coalition_without_i - j).all_subcoalitions():
                if game.get_value((S + i) + j) - game.get_value(
                    S + i
                ) < game.get_value(S + j) - game.get_value(S):
                    return False
    return True


def check_supermodularity(game: Game) -> bool:
    return check_convexity(game)
