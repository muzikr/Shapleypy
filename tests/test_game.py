from shapleypy.game import Game
from shapleypy.coalition import Coalition
import numpy as np

def test_init():
    game = Game(3)
    assert game.number_of_players == 3
    assert game._values.shape == (8,)
    #assert game._values == [0., np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

def test_str():
    game = Game(3)
    assert str(game) == """Game(number_of_players=3,
\tCoalition([]): 0.0,
\tCoalition([0]): nan,
\tCoalition([1]): nan,
\tCoalition([0, 1]): nan,
\tCoalition([2]): nan,
\tCoalition([0, 2]): nan,
\tCoalition([1, 2]): nan,
\tCoalition([0, 1, 2]): nan,
)"""

def test_set_value():
    game = Game(3)
    game.set_value([1, 2], 1.0)
    assert game._values[0b110] == 1.0
    #game.set_value(Coalition.from_players([0, 2]), 2.0)
    #assert game._values[0b101] == 2.0

