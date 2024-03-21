from __future__ import annotations

import warnings
from typing import Any

import numpy as np

from shapleypy._typing import Value, ValueInput
from shapleypy.constants import DEFAULT_VALUE, DEFAULT_VALUE_WARNING


def set_default_value(
    values_array: np.ndarray[Any, np.dtype[Value]],
    default_value: ValueInput | None,
) -> np.ndarray[Any, np.dtype[Value]]:
    """
    Set the default value to the missing values in the array for solution
    concepts calculations.
    """
    if default_value is None:
        value_to_use = DEFAULT_VALUE
    else:
        value_to_use = Value(default_value)

    used_default_value = False
    for i in range(len(values_array)):
        if np.isnan(values_array[i]):
            values_array[i] = value_to_use
            used_default_value = True

    if used_default_value and default_value is None:
        warnings.warn(DEFAULT_VALUE_WARNING, RuntimeWarning, stacklevel=2)

    return values_array
