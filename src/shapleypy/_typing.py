from __future__ import annotations

from collections.abc import Iterable
from typing import Union

import numpy as np

Player = int
Players = Iterable[Player]


Value = np.float64
ValueInput = Union[Value, float]
