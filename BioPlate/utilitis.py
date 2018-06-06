import numpy as np

from string import ascii_uppercase
from collections import namedtuple


_LETTER = np.array(list(ascii_uppercase))
Row =  namedtuple("R", ["start", "stop", "step", "C"])
Column = namedtuple("C", ["start", "stop", "step", "C"])
All = namedtuple("A", ["pos", "index"]) #pos = position
