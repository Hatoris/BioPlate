import numpy as np

from string import ascii_uppercase
from collections import namedtuple


_LETTER = np.array(list(ascii_uppercase))
#el for element
EL=  namedtuple("coordinate", ["pos", "row", "column"])
#Column = namedtuple("C", ["start", "stop", "step", "R"])
#All = namedtuple("A", ["pos", "index"]) #pos = position
#Puit = namedtuple("P", ["R", "C"])
