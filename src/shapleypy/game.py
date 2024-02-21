from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.protocols import Player, Value

Players = Iterable[Player]
Coalitions = Iterable[Coalition]


class Game:
    def __init__(self, number_of_players: int) -> None:
        self.number_of_players: int = number_of_players
        self._values: np.ndarray = np.zeros(2**number_of_players, dtype=Value)
        self._init_values()

    def set_value(
        self, coalition: Coalition | Players, value: Value | float
    ) -> None:
        """Set the value of a coalition."""
        if isinstance(coalition, Iterable):
            coalition = Coalition.from_players(coalition)
        self._values[coalition.id] = value

    def set_values(
        self, values: Iterable[tuple[Coalition | Players, Value | float]]
    ) -> None:
        """Set the values of multiple coalitions."""
        for coalition, value in values:
            self.set_value(coalition, value)

    def get_value(self, coalition: Coalition | Players) -> Value:
        """Get the value of a coalition."""
        if isinstance(coalition, Iterable):
            coalition = Coalition.from_players(coalition)
        return self._values[coalition.id]

    def get_values(
        self,
        coalitions: Iterable[Coalition | Players] | None = None,
    ) -> Iterable[tuple[Coalition, Value]]:
        """Get the values of multiple coalitions."""
        converted_coalitions = []
        if coalitions is None:
            converted_coalitions = list(
                Coalition.all_coalitions(self.number_of_players)
            )
        else:
            converted_coalitions = [
                (
                    Coalition.from_players(coalition)
                    if isinstance(coalition, Iterable)
                    else coalition
                )
                for coalition in coalitions
            ]
        yield from (
            (coalition, self.get_value(coalition))
            for coalition in converted_coalitions
        )

    def _init_values(self) -> None:
        self._values.fill(np.nan)
        empty_coalition = Coalition.from_players([])
        self.set_value(empty_coalition, Value(0.0))

    def __str__(self) -> str:
        to_return = f"Game(number_of_players={self.number_of_players},"
        for i in range(len(self._values)):
            to_return += f"\n\t{Coalition(i)}: {self._values[i]},"
        to_return += "\n)"
        return to_return

    def __repr__(self) -> str:
        to_return = f"Game(number_of_players={self.number_of_players},"
        for i in range(len(self._values)):
            to_return += f"\n\t{Coalition(i)!r}: {self._values[i]},"
        to_return += "\n)"
        return to_return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Game):
            return False

        if self.number_of_players != other.number_of_players:
            return False

        return all(
            a == b or (np.isnan(a) and np.isnan(b))
            for a, b in zip(self._values, other._values)
        )
