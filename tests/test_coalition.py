import numpy as np
import pytest

from shapleypy.coalition import Coalition


@pytest.fixture
def all_coalitions_of_4_players():
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


def test_repr():
    assert repr(Coalition(0b1010)) == "Coalition(id=1010)"


def test_str():
    assert str(Coalition(0b1010)) == "Coalition([1, 3])"


def test_len():
    assert len(Coalition(0b1010)) == 2


def test_hash():
    assert hash(Coalition(0b1010)) == hash(Coalition(0b1010))
    assert hash(Coalition(0b1010)) != hash(Coalition(0b1000))


def test_from_players():
    assert Coalition.from_players([1, 3]) == Coalition(0b1010)
    assert Coalition.from_players(1) == Coalition(0b10)
    with pytest.raises(ValueError):
        Coalition.from_players(33)
    with pytest.raises(ValueError):
        Coalition.from_players(0)


def test_get_players():
    assert list(Coalition(0b1010).get_players) == [1, 3]


def test_eq():
    assert Coalition(0b1010) == Coalition(0b1010)
    assert Coalition(0b1010) == [1, 3]
    assert not (Coalition(0b1010) == 5)


def test_contains():
    assert 1 in Coalition(0b1010)
    assert Coalition(0b1010) in Coalition(0b1111)
    assert 0 not in Coalition(0b1010)
    assert Coalition(0b1010) not in Coalition(0b0111)
    assert Coalition(0b1000) not in Coalition(0b0111)
    assert "s" not in Coalition(0b1010)


def test_grand_coalition():
    assert Coalition.grand_coalition(4) == Coalition(0b1111)
    assert Coalition.grand_coalition(32) == Coalition(np.uintc(4_294_967_295))
    assert Coalition.grand_coalition(1) == Coalition(0b1)
    with pytest.raises(ValueError):
        Coalition.grand_coalition(33)
    with pytest.raises(ValueError):
        Coalition.grand_coalition(0)


def test_all_subcoalitions(all_coalitions_of_4_players):
    assert list(Coalition(0b1010).all_subcoalitions()) == [
        Coalition(0b0010),
        Coalition(0b1000),
        Coalition(0b1010),
    ]
    assert (
        list(Coalition.grand_coalition(4).all_subcoalitions())
        == all_coalitions_of_4_players
    )


def test_all_coalitions(all_coalitions_of_4_players):
    assert list(Coalition.all_coalitions(4)) == all_coalitions_of_4_players
