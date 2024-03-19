from shapleypy._typing import Value

# Allowed number of players in a game.
MAXIMUM_NUMBER_OF_PLAYERS = 32
MINIMUM_NUMBER_OF_PLAYERS = 1

# Allowed player numbers (identifiers)
MAX_PLAYER = 31
MIN_PLAYER = 0

# Default value for a coalition for solution concepts
DEFAULT_VALUE = Value(0.0)

# Errors
COALITION_NUMBER_OF_PLAYERS_ERROR = "Number of players must be between 1 and 32"
GAME_COALITION_INPUT_ERROR = (
    "coalition must be a Coalition or an Iterable of Players"
)
LOADERS_MISSING_NUMBER_OF_PLAYERS_ERROR = (
    "The file does not contain the number of players."
)
CSV_SEPARATOR_ERROR = "csv_separator and coalition_separator cannot be the same"
CORE_POINT_ERROR = """
    The generator is not a point. If you managed to get this error, please
    report it to the developers.
    """
CORE_WINDOWS_ERROR = """
    The 'pplpy' package is required to use the core solution concept. But is
    not available for windows.
    """
POSITIVE_GAME_GENERATOR_LOWER_BOUND_ERROR = "lower_bound must be non-negative"
K_GAMES_PARAMETER = "k must be between 1 and the number of players"
CONVEX_GAME_GENERATOR_ERROR = "convex_game_generator is not available"

# Warnings
DEFAULT_VALUE_WARNING = "Warning: Unchanged default value is used in the game"
