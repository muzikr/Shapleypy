import ast
import json

from shapleypy.constants import LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR
from shapleypy.game import Game

def load_game_from_json(file: str) -> Game:
    n = None
    values = []
    with open(file) as f:
        data = json.load(f)
        if "n" not in data:
            raise ValueError(LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR)
        n = data["n"]
        if "values" in data:
            values_from_json = data["values"]
            values = [
                (ast.literal_eval(key), value)
                for key, value in values_from_json.items()
            ]
    game = Game(n)
    game.set_values(values)
    return game
