from typing import Dict, Iterable

import numpy as np

from shapleypy.coalition import Coalition
from shapleypy.protocols import Value, Player

class Game:
    def __init__(self, number_of_players: int) -> None:
        self.number_of_players: int = number_of_players
        self._values: np.ndarray = np.zeros(2 ** number_of_players, dtype=Value)
        self.__init_values()

    def set_value(self, coalition: Coalition | Iterable[Player], value: Value) -> None:
        if isinstance(coalition, Iterable):
            coalition = Coalition.from_players(coalition)
        self._values[coalition.id] = value

    def set_values(self, values: Dict[Iterable[Player], Value]) -> None:
        for coalition, value in values.items():
            self.set_value(Coalition.from_players(coalition), value)

    def __init_values(self) -> None:
        self._values.fill(np.nan)
        empty_coalition = Coalition.from_players([])
        self.set_value(empty_coalition, 0.0)

    def __str__(self) -> str:
        to_return = f"Game(number_of_players={self.number_of_players},"
        for i in range(len(self._values)):
            to_return += f"\n\t{Coalition(i)}: {self._values[i]},"
        to_return += "\n)"
        return to_return