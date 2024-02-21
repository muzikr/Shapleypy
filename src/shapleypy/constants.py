# Allowed number of players in a game.
MAXIMUM_NUMBER_OF_PLAYERS = 32
MINIMUM_NUMBER_OF_PLAYERS = 1

# Allowed player numbers (identifiers)
MAX_PLAYER = 31
MIN_PLAYER = 0

# Errors
COALITION_NUMBER_OF_PLAYERS_ERROR = "Number of players must be between 1 and 32"
LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR = (
    "The file does not contain the number of players."
)
LOADERS_CSV_SEPARATOR_ERROR = (
    "csv_separator and coalition_separator cannot be the same"
)
