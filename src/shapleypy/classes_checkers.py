# ruff: noqa: N806
from __future__ import annotations

from collections.abc import Callable

from shapleypy.coalition import (
    EMPTY_COALITION,
    Coalition,
    all_one_player_missing_subcoalitions,
)
from shapleypy.constants import K_GAMES_PARAMETER
from shapleypy.game import Game


def _determine_k_for_k_game(game: Game) -> int:
    """
    Determines the k parameter for a k-game.

    Args:
        game (Game): The game to determine the k parameter for.

    Returns:
        int: The determined k parameter.
    """
    for k in range(1, game.number_of_players + 1):
        if not all(
            game.get_value(S) == 0
            for S in filter(lambda s: len(s) == k, game.all_coalitions)
        ):
            return k
    # In case of zero game return number_of_players
    return k


def check_monotonicity(game: Game) -> bool:
    """
    Check if the game is monotone.

    Args:
        game (Game): The game to check.

    Returns:
        bool: True if the game is monotone, False otherwise.
    """
    for S in game.all_coalitions:
        # Check the values of all subcoalitions of size |S| - 1
        value_of_S = game.get_value(S)
        for S_minus_one in all_one_player_missing_subcoalitions(S):
            if value_of_S < game.get_value(S_minus_one):
                return False
    return True


def check_weakly_superadditivity(game: Game) -> bool:
    """
    Check if the game is weakly superadditive.

    Args:
        game (Game): The game to check.

    Returns:
        bool: True if the game is weakly superadditive, False otherwise.
    """
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    for i in range(game.number_of_players):
        value_of_i = game.get_value([i])
        for S in (grand_coalition - i).all_subcoalitions():
            if game.get_value(S) + value_of_i > game.get_value(S + i):
                return False
    return True


def check_superadditivity(game: Game) -> bool:
    """
    Check if the game is superadditive.

    Args:
        game (Game): The game to check.

    Returns:
        bool: True if the game is superadditive, False otherwise.
    """
    for T in game.all_coalitions:
        value_of_T = game.get_value(T)
        for S in filter(
            lambda s: T * s == EMPTY_COALITION, game.all_coalitions
        ):
            if value_of_T + game.get_value(S) > game.get_value(T + S):
                return False
    return True


def check_convexity(game: Game, tolerance: float = 1e-5) -> bool:
    """
    Check if the game is convex (supermodular).

    Args:
        game (Game): The game to check.
        tolerance (float): The tolerance for the check (floating arithmetric).

    Returns:
        bool: True if the game is convex, False otherwise.
    """
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    # We can use just i < j, because it the condition is symmetric
    # (if we exchange i and j, we get the same condition)
    for i in range(game.number_of_players - 1):
        grand_coalition_without_i = grand_coalition - i
        for j in range(i + 1, game.number_of_players):
            for S in (grand_coalition_without_i - j).all_subcoalitions():
                if tolerance + game.get_value((S + i) + j) - game.get_value(
                    S + i
                ) < game.get_value(S + j) - game.get_value(S):
                    return False
    return True


def check_supermodularity(game: Game) -> bool:
    """
    Check if the game is convex (supermodular).

    Args:
        game (Game): The game to check.

    Returns:
        bool: True if the game is convex, False otherwise.
    """
    return check_convexity(game)


def check_positivity(game: Game) -> bool:
    """
    Check if the game is positive.

    Args:
        game (Game): The game to check.

    Returns:
        bool: True if the game is positive, False otherwise.
    """
    for S in game.all_coalitions:
        m_S = 0
        size_of_S = len(S)
        for T in S.all_subcoalitions():
            m_S += (-1) ** (size_of_S - len(T)) * game.get_value(T)
        if m_S < 0:
            return False
    return True


def check_k_game(
    game: Game, k: int | None = None, epsilon: float = 1e-10
) -> bool:
    """
    Check if the game is a k-game.

    Args:
        game (Game): The game to check.
        k (int): The parameter k for the k-game. If None, it will be determined,
            but takes some computation time.

    Returns:
        bool: True if the game is a k-game, False otherwise.
    """
    if k is None:
        k = _determine_k_for_k_game(game)

    if not 0 < k <= game.number_of_players:
        raise ValueError(K_GAMES_PARAMETER)

    for S in filter(lambda s: len(s) != k, game.all_coalitions):
        if len(S) < k:
            if game.get_value(S) != 0:
                return False
        else:
            d_S = 0
            size_of_S = len(S)
            for T in S.all_subcoalitions():
                d_S += (-1) ** (size_of_S - len(T)) * game.get_value(T)
            if not 0 - epsilon <= d_S <= 0 + epsilon:
                return False
    return True


def check_k_additivity(game: Game, k: int, epsilon: float = 1e-10) -> bool:
    """
    Check if the game is k-additive.

    Args:
        game (Game): The game to check.
        k (int): The parameter k for the k-additive game.
        epsilon (float): The tolerance for the check (floating arithmetric).

    Returns:
        bool: True if the game is k-additive, False otherwise.
    """
    if not 0 < k <= game.number_of_players:
        raise ValueError(K_GAMES_PARAMETER)

    for S in filter(lambda s: len(s) > k, game.all_coalitions):
        d_S = 0
        size_of_S = len(S)
        for T in S.all_subcoalitions():
            d_S += (-1) ** (size_of_S - len(T)) * game.get_value(T)
        if not 0 - epsilon <= d_S <= 0 + epsilon:
            return False
    return True


def determine_class(game: Game) -> str:
    """
    Determine the class of the game from standart hierarchy.

    Args:
        game (Game): The game to determine the class for.

    Returns:
        str: The class of the game (just the highest the game belongs to).
            (Positive, convex, superadditive, weakly superadditive, monotone,
            none)
    """
    checks: list[tuple[str, Callable[[Game], bool]]] = [
        ("Positive", check_positivity),
        ("Convex", check_convexity),
        ("Superadditive", check_superadditivity),
        ("Weakly superadditive", check_weakly_superadditivity),
        ("Monotone", check_monotonicity),
    ]

    for cls, check_func in checks:
        if check_func(game):
            return cls

    return "None"
