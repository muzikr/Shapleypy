from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy.constants import (
    COALITION_NUMBER_OF_PLAYERS_ERROR,
    MAX_PLAYER,
    MAXIMUM_NUMBER_OF_PLAYERS,
    MIN_PLAYER,
    MINIMUM_NUMBER_OF_PLAYERS,
)
from shapleypy.protocols import Player


class Coalition:
    def __init__(self, id: np.uintc) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f"Coalition(id={np.binary_repr(self.id)})"

    def __str__(self) -> str:
        return f"Coalition({list(self.get_players)})"

    def __len__(self) -> int:
        return bin(self.id).count("1")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coalition):
            return self.id == other.id
        elif isinstance(other, Iterable):
            return self.id == Coalition.from_players(other).id
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def __contains__(self, other: Player | Coalition) -> bool:
        if isinstance(other, Player):
            return bool(self.id & (1 << other))
        elif isinstance(other, Coalition):
            return (self.id & other.id) == other.id
        return False

    @staticmethod
    def from_players(players: Iterable[Player] | Player) -> Coalition:
        """Create a coalition from a list of players or a single player"""
        if isinstance(players, Player):
            players = [players]
        players = set(players)
        id = np.uintc(0)
        for player in players:
            if player > MAX_PLAYER or player < MIN_PLAYER:
                raise ValueError(COALITION_NUMBER_OF_PLAYERS_ERROR)
            id |= 1 << player
        return Coalition(id)

    @property
    def get_players(self) -> Iterable[Player]:
        """Return a list of players in the coalition"""
        bit_map = self.id
        index = 0

        while bit_map:
            if bit_map & 1:
                yield index
            bit_map >>= 1
            index += 1

    @staticmethod
    def grand_coalition(n_players: int) -> Coalition:
        """Return the grand coalition of n_players"""
        if (
            n_players > MAXIMUM_NUMBER_OF_PLAYERS
            or n_players < MINIMUM_NUMBER_OF_PLAYERS
        ):
            raise ValueError(COALITION_NUMBER_OF_PLAYERS_ERROR)
        return Coalition((1 << n_players) - 1)

    def all_subcoalitions(self) -> Iterable[Coalition]:
        """Return all subcoalitions of the coalition"""
        for i in range(1, self.id + 1):
            if self.id & i == i:
                yield Coalition(i)

    @staticmethod
    def all_coalitions(n_players: int) -> Iterable[Coalition]:
        """Return all coalitions of a game of n_players"""
        return Coalition.grand_coalition(n_players).all_subcoalitions()
