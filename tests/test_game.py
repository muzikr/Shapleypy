import numpy as np
import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game


@pytest.fixture
def basic_values_for_game_of_three_coalition_form() -> (
    list[tuple[Coalition, float]]
):
    return [
        (Coalition.from_players([0]), 1.0),
        (Coalition.from_players([1]), 2.0),
        (Coalition.from_players([0, 1]), 3.0),
        (Coalition.from_players([2]), 4.0),
        (Coalition.from_players([0, 2]), 5.0),
        (Coalition.from_players([1, 2]), 6.0),
        (Coalition.from_players([0, 1, 2]), 7.0),
    ]


@pytest.fixture
def basic_values_for_game_of_three_list_form() -> list[tuple[list[int], float]]:
    return [
        ([0], 1.0),
        ([1], 2.0),
        ([0, 1], 3.0),
        ([2], 4.0),
        ([0, 2], 5.0),
        ([1, 2], 6.0),
        ([0, 1, 2], 7.0),
    ]


def test_init() -> None:
    game = Game(3)
    assert game.number_of_players == 3
    assert game._values.shape == (8,)
    assert game._values[0] == 0.0
    assert all(np.isnan(x) for x in game._values[1:])


def test_str() -> None:
    game = Game(3)
    assert (
        str(game)
        == """Game(number_of_players=3,
\tCoalition([]): 0.0,
\tCoalition([0]): nan,
\tCoalition([1]): nan,
\tCoalition([0, 1]): nan,
\tCoalition([2]): nan,
\tCoalition([0, 2]): nan,
\tCoalition([1, 2]): nan,
\tCoalition([0, 1, 2]): nan,
)"""
    )


def test_repr() -> None:
    game = Game(3)
    assert (
        repr(game)
        == """Game(number_of_players=3,
\tCoalition(id=0): 0.0,
\tCoalition(id=1): nan,
\tCoalition(id=10): nan,
\tCoalition(id=11): nan,
\tCoalition(id=100): nan,
\tCoalition(id=101): nan,
\tCoalition(id=110): nan,
\tCoalition(id=111): nan,
)"""
    )


def test_set_value() -> None:
    game = Game(3)
    game.set_value([1, 2], 1.0)
    assert game._values[0b110] == 1.0
    game.set_value(Coalition.from_players([0, 2]), 2.0)
    assert game._values[0b101] == 2.0


def test_set_values_from_coalition_form(
    basic_values_for_game_of_three_coalition_form: list[
        tuple[Coalition, float]
    ],
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    assert all(
        a == b
        for a, b in zip(game._values, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    )


def test_set_values_from_str_form(
    basic_values_for_game_of_three_list_form: list[tuple[list[int], float]]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_list_form)
    assert all(
        a == b
        for a, b in zip(game._values, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    )


def test_get_value() -> None:
    game = Game(3)
    game.set_value([1, 2], 1.0)
    assert game.get_value([1, 2]) == 1.0
    game.set_value(Coalition.from_players([0, 2]), 2.0)
    assert game.get_value(Coalition.from_players([0, 2])) == 2.0
    assert np.isnan(game.get_value([0, 1, 2]))
    assert game.get_value(Coalition.from_players([])) == 0.0


def test_get_values(
    basic_values_for_game_of_three_coalition_form: list[tuple[Coalition, float]]
) -> None:
    game = Game(3)
    game.set_values(basic_values_for_game_of_three_coalition_form)
    assert (
        list(game.get_values()) == basic_values_for_game_of_three_coalition_form
    )

    assert list(
        game.get_values(
            [Coalition.from_players([0, 1]), Coalition.from_players([0, 2])]
        )
    ) == [
        (Coalition.from_players([0, 1]), 3),
        (Coalition.from_players([0, 2]), 5),
    ]
    assert list(game.get_values([Coalition.from_players([0, 1]), [0, 2]])) == [
        (Coalition.from_players([0, 1]), 3),
        (Coalition.from_players([0, 2]), 5),
    ]
    assert list(game.get_values([[0, 1], [0, 2]])) == [
        (Coalition.from_players([0, 1]), 3),
        (Coalition.from_players([0, 2]), 5),
    ]
    assert list(
        game.get_values([Coalition.from_players([0, 1]), [0, 2], [1, 2]])
    ) == [
        (Coalition.from_players([0, 1]), 3),
        (Coalition.from_players([0, 2]), 5),
        (Coalition.from_players([1, 2]), 6),
    ]
    assert list(
        game.get_values(
            [Coalition.from_players([0, 1]), [0, 2], [1, 2], [0, 1, 2]]
        )
    ) == [
        (Coalition.from_players([0, 1]), 3),
        (Coalition.from_players([0, 2]), 5),
        (Coalition.from_players([1, 2]), 6),
        (Coalition.from_players([0, 1, 2]), 7),
    ]
    assert list(
        game.get_values(
            [Coalition.from_players([0, 1]), [0, 2], [1, 2], [0, 1, 2]]
        )
    ) == [
        (Coalition.from_players([0, 1]), 3),
        (Coalition.from_players([0, 2]), 5),
        (Coalition.from_players([1, 2]), 6),
        (Coalition.from_players([0, 1, 2]), 7),
    ]


def set_value_out_of_bounds() -> None:
    game = Game(3)
    with pytest.raises(IndexError):
        game.set_value([0, 1, 2, 3], 1.0)
    with pytest.raises(IndexError):
        game.set_value(Coalition.from_players([0, 1, 2, 3]), 1.0)


def set_values_out_of_bounds() -> None:
    game = Game(3)
    with pytest.raises(IndexError):
        game.set_values(
            [
                (Coalition.from_players(0), 6.0),
                (Coalition.from_players([0, 1, 2, 3]), 1.0),
            ]
        )


def test_get_value_out_of_bounds() -> None:
    game = Game(3)
    with pytest.raises(IndexError):
        game.get_value([0, 1, 2, 3])
    with pytest.raises(IndexError):
        game.get_value(Coalition.from_players([0, 1, 2, 3]))


def test_get_values_out_of_bounds() -> None:
    game = Game(3)

    with pytest.raises(IndexError):
        list(
            game.get_values(
                [
                    Coalition.from_players([0, 1, 2, 3]),
                    [0, 2],
                    [1, 2],
                    [0, 1, 2],
                ]
            )
        )
    with pytest.raises(IndexError):
        list(game.get_values([[0, 1, 2, 3], [0, 2], [1, 2], [0, 1, 2]]))


def test_eq(
    basic_values_for_game_of_three_coalition_form: list[tuple[Coalition, float]]
) -> None:
    game1 = Game(3)
    game2 = Game(3)
    assert game1 == game2
    assert game1 != "hello"
    game2.set_value([1, 2], 1.0)
    assert game1 != game2
    game1.set_values(basic_values_for_game_of_three_coalition_form)
    game2.set_values(basic_values_for_game_of_three_coalition_form)
    assert game1 == game2
    game1 = Game(3)
    game2 = Game(4)
    assert game1 != game2
