from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy._typing import Player, Players
from shapleypy.constants import (
    COALITION_NUMBER_OF_PLAYERS_ERROR,
    MAX_PLAYER,
    MAXIMUM_NUMBER_OF_PLAYERS,
    MIN_PLAYER,
    MINIMUM_NUMBER_OF_PLAYERS,
)


class Coalition:
    """
    Represents a coalition of players in a game.

    Attributes:
        id (np.uint32): The ID of the coalition.

    Methods:
        from_players: Creates a coalition from a list of players.
        get_players: Returns an iterator of players in the coalition.
        grand_coalition: Returns the grand coalition with a specified number of
            players.
        all_subcoalitions: Returns an iterator of all subcoalitions of the
            coalition.
        all_coalitions: Returns an iterator of all coalitions with a specified
            number of players.
    """

    def __init__(self, id: int | np.uint32) -> None:
        """
        Initialize a Coalition object with the given ID.

        Args:
            id (int | np.uint32): The ID (bitmap) of the coalition.

        Returns:
            None
        """
        if isinstance(id, int):
            self.id = np.uint32(id)
        elif isinstance(id, np.uint32):
            self.id = id

    def __repr__(self) -> str:
        """
        Returns a string representation of the Coalition object.

        Returns:
            str: The string representation of the Coalition object (bitmaps).
        """
        return f"Coalition(id={np.binary_repr(self.id)})"

    def __str__(self) -> str:
        """
        Returns a string representation of the Coalition object.

        Returns:
            str: The string representation of the Coalition object
                (list of players).
        """
        return f"Coalition({list(self.get_players)})"

    def __len__(self) -> int:
        """
        Returns the number of players in the coalition.

        Returns:
            int: The number of players in the coalition.
        """
        return bin(self.id).count("1")

    def __eq__(self, other: object) -> bool:
        """
        Compares the coalition object with another object for equality.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(other, Coalition):
            return self.id == other.id
        elif isinstance(other, Player):
            return self.id == Coalition.from_players([other]).id
        elif isinstance(other, Iterable) and all(
            isinstance(i, Player) for i in other
        ):
            return self.id == Coalition.from_players(other).id
        return False

    def __hash__(self) -> int:
        """
        Returns the hash of the coalition.

        Returns:
            int: The hash of the coalition (hash of the ID (bitmap)).
        """
        return hash(self.id)

    def __contains__(self, other: object) -> bool:
        """
        Checks if the coalition contains a player or another coalition as
        subcoalition.

        Args:
            other (object): The player or coalition to check.

        Returns:
            bool: True if the player or coalition is in the coalition,
                False otherwise.
        """
        if isinstance(other, Player):
            return bool(self.id & (1 << other))
        elif isinstance(other, Iterable) and all(
            isinstance(i, Player) for i in other
        ):
            return (
                self.id & Coalition.from_players(other).id
            ) == Coalition.from_players(other).id
        elif isinstance(other, Coalition):
            return (self.id & other.id) == other.id
        return False

    def __add__(self, other: object) -> Coalition:
        """
        Unites two objects and returns a new Coalition object.

        Args:
            other (object): The object to be united with.

        Returns:
            Coalition: A new Coalition object resulting from the union.

        Raises:
            TypeError: If the object being united is not of a supported type
                (Player, Coalition, or Iterable of Players).
        """
        if isinstance(other, Player):
            return Coalition(self.id | Coalition.from_players([other]).id)
        elif isinstance(other, Coalition):
            return Coalition(self.id | other.id)
        elif isinstance(other, Iterable) and all(
            isinstance(i, Player) for i in other
        ):
            return Coalition(self.id | Coalition.from_players(other).id)
        raise TypeError

    def __sub__(self, other: object) -> Coalition:
        """
        Subtract the given object from this coalition (set subtracion).

        Args:
            other (object): The object to subtract from this coalition.

        Returns:
            Coalition: A new Coalition object resulting from the subtraction.

        Raises:
            TypeError: If the object being subtracted is not of a supported type
                (Player, Coalition, or Iterable of Players).
        """
        if isinstance(other, Player):
            return Coalition(self.id & ~Coalition.from_players([other]).id)
        elif isinstance(other, Coalition):
            return Coalition(self.id & ~other.id)
        elif isinstance(other, Iterable) and all(
            isinstance(i, Player) for i in other
        ):
            return Coalition(self.id & ~Coalition.from_players(other).id)
        raise TypeError

    def __mul__(self, other: object) -> Coalition:
        """
        Intersect the current coalition with another object.

        Args:
            other (object): The object to intersect with.

        Returns:
            Coalition: The result of the intersection.

        Raises:
            TypeError: If the object being intersected is not of a supported
                type (Player, Coalition, or Iterable of Players).
        """
        if isinstance(other, Player):
            return Coalition(self.id & Coalition.from_players([other]).id)
        elif isinstance(other, Coalition):
            return Coalition(self.id & other.id)
        elif isinstance(other, Iterable) and all(
            isinstance(i, Player) for i in other
        ):
            return Coalition(self.id & Coalition.from_players(other).id)
        raise TypeError

    def __truediv__(self, other: object) -> Coalition:
        """
        Symmetric difference of the current coalition and another object.

        Args:
            other (object): The object to be symmetrically differenced with.

        Returns:
            Coalition: The resulting coalition after the symmetric difference.

        Raises:
            TypeError: If the object being symmetrically differenced is not of a
                supported type (Player, Coalition, or Iterable of Players).
        """
        if isinstance(other, Player):
            return Coalition(self.id ^ Coalition.from_players([other]).id)
        elif isinstance(other, Coalition):
            return Coalition(self.id ^ other.id)
        elif isinstance(other, Iterable) and all(
            isinstance(i, Player) for i in other
        ):
            return Coalition(self.id ^ Coalition.from_players(other).id)
        raise TypeError

    @staticmethod
    def from_players(players: Players | Player) -> Coalition:
        """
        Creates a coalition from a list of players or single player.

        Args:
            players (Players | Player): The list of players or a single player.

        Returns:
            Coalition: The created coalition with proper ID (bitmap) set.

        Raises:
            ValueError: If the player number is invalid (too high or low).
        """
        if isinstance(players, Player):
            players = [players]
        players = set(players)
        id = 0
        for player in players:
            if player > MAX_PLAYER or player < MIN_PLAYER:
                raise ValueError(COALITION_NUMBER_OF_PLAYERS_ERROR)
            id |= 1 << player
        return Coalition(id)

    @property
    def get_players(self) -> Players:
        """
        Returns an iterator of players in the coalition.

        Yields:
            int: The player numbers in the coalition.
        """
        bit_map = int(self.id)
        index = 0

        while bit_map:
            if bit_map & 1:
                yield index
            bit_map >>= 1
            index += 1

    @staticmethod
    def grand_coalition(n_players: int) -> Coalition:
        """
        Returns the grand coalition with a specified number of players.

        Args:
            n_players (int): The number of players.

        Returns:
            Coalition: The grand coalition.

        Raises:
            ValueError: If the number of players is invalid (too hight or low).
        """
        if (
            n_players > MAXIMUM_NUMBER_OF_PLAYERS
            or n_players < MINIMUM_NUMBER_OF_PLAYERS
        ):
            raise ValueError(COALITION_NUMBER_OF_PLAYERS_ERROR)
        return Coalition((1 << n_players) - 1)

    def all_subcoalitions(self) -> Iterable[Coalition]:
        """
        Returns an iterator of all subcoalitions of the coalition.

        Yields:
            Coalition: The subcoalitions of the coalition.
        """
        for i in range(1, self.id + 1):
            if self.id & i == i:
                yield Coalition(i)

    @staticmethod
    def all_coalitions(n_players: int) -> Iterable[Coalition]:
        """
        Returns an iterator of all coalitions with a specified number of
        players.

        Args:
            n_players (int): The number of players.

        Yields:
            Coalition: The coalitions with the specified number of players.

        Raises:
            ValueError: If the number of players is invalid (too high or low).
        """
        return Coalition.grand_coalition(n_players).all_subcoalitions()


def all_one_player_missing_subcoalitions(
    coalition: Coalition,
) -> Iterable[Coalition]:
    """
    Returns an iterator of all subcoalitions with one player removed from the
    given coalition (coalitions of size len(coalition) - 1).

    Args:
        coalition (Coalition): The coalition to generate subcoalitions from.

    Yields:
        Coalition: The subcoalitions of the given coalition with one player
            removed.
    """
    for i in coalition.get_players:
        yield coalition - i


EMPTY_COALITION = Coalition(0)
