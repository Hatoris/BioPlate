from typing import NamedTuple

from collections import namedtuple
from string import ascii_uppercase

import numpy as np

_LETTER : np.ndarray = np.array(list(ascii_uppercase))
# el for element
EL : NamedTuple = namedtuple("coordinate", ["pos", "row", "column"])
