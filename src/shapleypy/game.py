from typing import Iterable, List, Tuple

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

    def set_value(self, coalition: Coalition | Players, value: Value) -> None:
        """Set the value of a coalition."""
        if isinstance(coalition, Iterable):
            coalition = Coalition.from_players(coalition)
        self._values[coalition.id] = value

    def set_values(
        self,
        values: Iterable[Tuple[Coalition, Value]]
        | Iterable[Tuple[Players, Value]],
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
        coalitions: Coalitions | Iterable[Players] | None = None,
    ) -> Iterable[Tuple[Coalition, Value]]:
        """Get the values of multiple coalitions."""
        if coalitions is None:
            coalitions = list(Coalition.all_coalitions(self.number_of_players))
        else:
            coalitions = [
                Coalition.from_players(coalition)
                if isinstance(coalition, List)
                else coalition
                for coalition in coalitions
            ]
        yield from (
            (coalition, self.get_value(coalition)) for coalition in coalitions
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
        if self.number_of_players != other.number_of_players:
            return False

        return all(
            a == b or (np.isnan(a) and np.isnan(b))
            for a, b in zip(self._values, other._values)
        )
