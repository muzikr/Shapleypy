import ast
import csv
import json

from shapleypy.constants import (
    CSV_SEPARATOR_ERROR,
    LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR,
)
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


def load_game_from_csv(
    file: str, csv_separator: str = ":", coalition_separator: str = ","
) -> Game:
    if csv_separator == coalition_separator:
        raise ValueError(CSV_SEPARATOR_ERROR)

    n = None
    values = []
    with open(file, newline="") as f:
        reader = csv.reader(f, delimiter=csv_separator)
        for row in reader:
            if len(row) > 0:
                if row[0] == "n":
                    n = int(row[1])
                else:
                    key_list = list(map(int, row[0].split(coalition_separator)))
                    value = float(row[1])
                    values.append((key_list, value))
    if n is None:
        raise ValueError(LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR)
    game = Game(n)
    game.set_values(values)
    return game
