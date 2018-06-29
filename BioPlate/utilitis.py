from typing import NamedTuple, Union

from collections import namedtuple
from string import ascii_uppercase

import numpy as np
import re

_LETTER: np.ndarray = np.array(list(ascii_uppercase))
_CP1 = re.compile("(\d+)")
_CP2 = re.compile("([A-Za-z])")
_CP3 = re.compile("(\w+[\-|\,]\w+)")

# el for element
EL = NamedTuple(
    "coordinate",
    [("pos", str), ("row", Union[int, slice]), ("column", Union[int, slice])],
)
