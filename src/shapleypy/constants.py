# Allowed number of players in a game.
MAXIMUM_NUMBER_OF_PLAYERS = 32
MINIMUM_NUMBER_OF_PLAYERS = 1

# Allowed player numbers (identifiers)
MAX_PLAYER = 31
MIN_PLAYER = 0

# Default value for a coalition for solution concepts
DEFAULT_VALUE = 0.0

# Errors
COALITION_NUMBER_OF_PLAYERS_ERROR = "Number of players must be between 1 and 32"
LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR = (
    "The file does not contain the number of players."
)
CSV_SEPARATOR_ERROR = "csv_separator and coalition_separator cannot be the same"

# Warnings
DEFAULT_VALUE_WARNING = "Warning: Unchanged default value is used in the game"
