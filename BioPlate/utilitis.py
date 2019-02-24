from typing import NamedTuple, Union

from collections import namedtuple
from string import ascii_uppercase

import numpy as np
import re

_LETTER: np.ndarray = np.array(list(ascii_uppercase))
_FIND_LEFT_RIGHT = re.compile(r"\w+[\-|\,]\w+|[A-Za-z]|\d+")
_SPECIAL_CHAR = re.compile(r"\W")
_FIND_ZERO = re.compile("(^0$|(?<!\d)0)")

# el for element
EL = NamedTuple(
    "coordinate",
    [("pos", str), ("row", Union[int, slice]), ("column", Union[int, slice])],
)
