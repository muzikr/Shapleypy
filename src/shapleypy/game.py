from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from shapleypy._typing import Player, Players, Value, ValueInput
from shapleypy.coalition import Coalition
from shapleypy.constants import GAME_COALITION_INPUT_ERROR

Coalitions = Iterable[Coalition]


class Game:
    """
    Represents a game with a specified number of players.

    Attributes:
        number_of_players (int): The number of players in the game.
        _values (np.ndarray): An array to store the values of coalitions.

    Methods:
        set_value: Sets the value of a coalition.
        set_values: Sets the values of multiple coalitions.
        get_value: Retrieves the value of a coalition.
        get_values: Retrieves the values of specified coalitions.
        _init_values: Initializes the values of the coalitions to np.nan for all
            coalitions without empty coalition which is set to zero.
    """

    def __init__(self, number_of_players: int) -> None:
        """
        Initializes a new instance of the Game class.

        Args:
            number_of_players (int): The number of players in the game.
        """
        self.number_of_players: int = number_of_players
        self._values: np.ndarray = np.zeros(2**number_of_players, dtype=Value)
        self._init_values()

    def set_value(
        self, coalition: Coalition | Players | Player, value: ValueInput
    ) -> None:
        """
        Sets the value of a coalition.

        Args:
            coalition (Coalition | Players | Player): The coalition or player(s)
                for which to set the value.
            value (ValueInput): The value to set.

        Raises:
            TypeError: If the coalition input is not of the correct type
                (listed above).

        Returns:
            None
        """
        final_coalition = coalition
        if isinstance(coalition, Player):
            final_coalition = Coalition.from_players([coalition])
        elif isinstance(coalition, Iterable) and all(
            isinstance(i, Player) for i in coalition
        ):
            final_coalition = Coalition.from_players(coalition)
        if not isinstance(final_coalition, Coalition):
            raise TypeError(GAME_COALITION_INPUT_ERROR)
        self._values[final_coalition.id] = value

    def set_values(
        self, values: Iterable[tuple[Coalition | Players, ValueInput]]
    ) -> None:
        """
        Sets the values of multiple coalitions.

        Args:
            values (Iterable[tuple[Coalition | Players, ValueInput]]):
                The coalitions and values to set.

        Returns:
            None
        """
        for coalition, value in values:
            self.set_value(coalition, value)

    def get_value(self, coalition: Coalition | Players | Player) -> Value:
        """
        Retrieves the value of a coalition.

        Args:
            coalition (Coalition | Players | Player): The coalition or player(s)
                for which to retrieve the value.

        Raises:
            TypeError: If the coalition input is not of the correct type.

        Returns:
            Value: The value of the coalition.
        """
        final_coalition = coalition
        if isinstance(coalition, Player):
            final_coalition = Coalition.from_players([coalition])
        elif isinstance(coalition, Iterable) and all(
            isinstance(i, Player) for i in coalition
        ):
            final_coalition = Coalition.from_players(coalition)
        if not isinstance(final_coalition, Coalition):
            raise TypeError(GAME_COALITION_INPUT_ERROR)
        return self._values[final_coalition.id]

    def get_values(
        self,
        coalitions: Iterable[Coalition | Players] | None = None,
    ) -> Iterable[tuple[Coalition, Value]]:
        """
        Retrieves the values of specified coalitions.

        Args:
            coalitions (Iterable[Coalition | Players] | None): The coalitions or
                player(s) for which to retrieve the values.
                If None, retrieves the values of all possible coalitions.

        Raises:
            TypeError: If the coalition input is not of the correct type.

        Yields:
            tuple[Coalition, Value]: The coalition and its corresponding value.
        """
        converted_coalitions = []
        if coalitions is None:
            converted_coalitions = list(
                Coalition.all_coalitions(self.number_of_players)
            )
        else:
            for coalition in coalitions:
                if isinstance(coalition, Iterable) and all(
                    isinstance(i, Player) for i in coalition
                ):
                    converted_coalitions.append(
                        Coalition.from_players(coalition)
                    )
                elif isinstance(coalition, Coalition):
                    converted_coalitions.append(coalition)
                else:
                    raise TypeError(GAME_COALITION_INPUT_ERROR)
        yield from (
            (coalition, self.get_value(coalition))
            for coalition in converted_coalitions
        )

    def _init_values(self) -> None:
        """
        Initializes the values of the coalitions.

        Returns:
            None
        """
        self._values.fill(np.nan)
        empty_coalition = Coalition.from_players([])
        self.set_value(empty_coalition, Value(0.0))

    def __str__(self) -> str:
        """
        Returns a string representation of the Game object.

        Returns:
            str: The string representation of the Game object.
        """
        to_return = f"Game(number_of_players={self.number_of_players},"
        for i in range(len(self._values)):
            to_return += f"\n\t{Coalition(i)}: {self._values[i]},"
        to_return += "\n)"
        return to_return

    def __repr__(self) -> str:
        """
        Returns a string representation of the Game object.

        Returns:
            str: The string representation of the Game object.
        """
        to_return = f"Game(number_of_players={self.number_of_players},"
        for i in range(len(self._values)):
            to_return += f"\n\t{Coalition(i)!r}: {self._values[i]},"
        to_return += "\n)"
        return to_return

    def __eq__(self, other: object) -> bool:
        """
        Compares the Game object with another object for equality.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, Game):
            return False

        if self.number_of_players != other.number_of_players:
            return False

        return all(
            a == b or (np.isnan(a) and np.isnan(b))
            for a, b in zip(self._values, other._values)
        )

    @property
    def all_coalitions(self) -> Coalitions:
        """
        Returns all possible coalitions for the game.

        Returns:
            Coalitions: An object representing all possible coalitions.
        """
        return Coalition.all_coalitions(self.number_of_players)
