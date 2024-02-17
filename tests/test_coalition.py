import pytest

from shapleypy.coalition import Coalition


@pytest.fixture
def all_coalitions_of_4_players() -> list[Coalition]:
    return [
        Coalition(0b0001),
        Coalition(0b0010),
        Coalition(0b0011),
        Coalition(0b0100),
        Coalition(0b0101),
        Coalition(0b0110),
        Coalition(0b0111),
        Coalition(0b1000),
        Coalition(0b1001),
        Coalition(0b1010),
        Coalition(0b1011),
        Coalition(0b1100),
        Coalition(0b1101),
        Coalition(0b1110),
        Coalition(0b1111),
    ]


def test_repr() -> None:
    assert repr(Coalition(0b1010)) == "Coalition(id=1010)"


def test_str() -> None:
    assert str(Coalition(0b1010)) == "Coalition([1, 3])"


def test_len() -> None:
    assert len(Coalition(0b1010)) == 2


def test_hash() -> None:
    assert hash(Coalition(0b1010)) == hash(Coalition(0b1010))
    assert hash(Coalition(0b1010)) != hash(Coalition(0b1000))


def test_from_players() -> None:
    assert Coalition.from_players([1, 3]) == Coalition(0b1010)
    assert Coalition.from_players(1) == Coalition(0b10)
    assert Coalition.from_players(0) == Coalition(0b1)
    assert Coalition.from_players(31) == Coalition(
        0b10000000000000000000000000000000
    )
    with pytest.raises(ValueError):
        Coalition.from_players(32)
    with pytest.raises(ValueError):
        Coalition.from_players(-1)


def test_get_players() -> None:
    assert list(Coalition(0b1010).get_players) == [1, 3]
    assert list(Coalition(0b1).get_players) == [0]
    assert list(Coalition(0b10000000000000000000000000000000).get_players) == [
        31
    ]


def test_eq() -> None:
    assert Coalition(0b1010) == Coalition(0b1010)
    assert Coalition(0b1010) == [1, 3]
    assert not (Coalition(0b1010) == 5)


def test_contains() -> None:
    assert 1 in Coalition(0b1010)
    assert Coalition(0b1010) in Coalition(0b1111)
    assert 0 not in Coalition(0b1010)
    assert Coalition(0b1010) not in Coalition(0b0111)
    assert Coalition(0b1000) not in Coalition(0b0111)
    assert "s" not in Coalition(0b1010)


def test_grand_coalition() -> None:
    assert Coalition.grand_coalition(4) == Coalition(0b1111)
    assert Coalition.grand_coalition(32) == Coalition(4_294_967_295)
    assert Coalition.grand_coalition(1) == Coalition(0b1)
    with pytest.raises(ValueError):
        Coalition.grand_coalition(33)
    with pytest.raises(ValueError):
        Coalition.grand_coalition(0)


def test_all_subcoalitions(
    all_coalitions_of_4_players: list[Coalition],
) -> None:
    assert list(Coalition(0b1010).all_subcoalitions()) == [
        Coalition(0b0010),
        Coalition(0b1000),
        Coalition(0b1010),
    ]
    assert (
        list(Coalition.grand_coalition(4).all_subcoalitions())
        == all_coalitions_of_4_players
    )


def test_all_coalitions(all_coalitions_of_4_players: list[Coalition]) -> None:
    assert list(Coalition.all_coalitions(4)) == all_coalitions_of_4_players


def test_add() -> None:
    assert Coalition(0b1010) + Coalition(0b0100) == Coalition(0b1110)
    assert Coalition(0b1010) + [0, 2] == Coalition(0b1111)  # noqa RUF005
    assert Coalition(0b1010) + 0 == Coalition(0b1011)
    assert Coalition(0b1010) + Coalition(0b0010) == Coalition(0b1010)
    with pytest.raises(TypeError):
        Coalition(0b1010) + "s"


def test_sub() -> None:
    assert Coalition(0b1010) - Coalition(0b0100) == Coalition(0b1010)
    assert Coalition(0b1010) - [3, 1] == Coalition(0b0000)
    assert Coalition(0b1010) - 3 == Coalition(0b0010)
    assert Coalition(0b1010) - Coalition(0b0010) == Coalition(0b1000)
    with pytest.raises(TypeError):
        Coalition(0b1010) - "s"


def test_intersection() -> None:
    assert Coalition(0b1010) * Coalition(0b0100) == Coalition(0b0000)
    assert Coalition(0b1010) * [3, 0] == Coalition(0b1000)
    assert Coalition(0b1010) * 3 == Coalition(0b1000)
    assert Coalition(0b1010) * Coalition(0b0010) == Coalition(0b0010)
    with pytest.raises(TypeError):
        Coalition(0b1010) * "s"


def test_symmetric_difference() -> None:
    assert Coalition(0b1010) / Coalition(0b0100) == Coalition(0b1110)
    assert Coalition(0b1010) / [3, 0] == Coalition(0b0011)
    assert Coalition(0b1010) / 2 == Coalition(0b1110)
    assert Coalition(0b1010) / Coalition(0b0010) == Coalition(0b1000)
    with pytest.raises(TypeError):
        Coalition(0b1010) / "s"
