from __future__ import annotations

from shapleypy.coalition import Coalition, all_one_player_missing_subcoalitions
from shapleypy.game import Game


def check_monotonicity(game: Game) -> bool:
    """
    Check if the game is monotone.
    """
    for coalition in game.all_coalitions:
        for coalition_without_player in all_one_player_missing_subcoalitions(
            coalition
        ):
            if game.get_value(coalition) < game.get_value(
                coalition_without_player
            ):
                return False
    return True


def check_weakly_superadditivity(game: Game) -> bool:
    grand_coalition = Coalition.grand_coalition(game.number_of_players)
    for i in range(game.number_of_players):
        for coalition in (grand_coalition - i).all_subcoalitions():
            if game.get_value(coalition) + game.get_value([i]) > game.get_value(
                coalition + i
            ):
                return False
    return True
