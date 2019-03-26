from typing import (
    Dict,
    List,
    Tuple,
    Optional,
    Union,
    Any,
    overload,
    Sequence,
    Generator,
    Callable,
)

import numpy as np

from BioPlate.core.array import Array
from BioPlate.core.manipulation import BioPlateManipulation
from BioPlate.core.matrix import BioPlateMatrix
from BioPlate.object.stack import Stack
from BioPlate.core.index import Index


class Inserts(Array, BioPlateManipulation):
    def __new__(cls, *args, **kwargs):
        kwargs.pop("inserts", None)
        return Array.__new__(cls, *args, inserts=True, **kwargs)

    def __init__(self: "Inserts", *args, **kwargs) -> None:
        self.ID = id(self)
        self._ind = {"top": 0, "bot": 1, "0": 0, "1": 1, 0: 0, 1: 1}

    def __add__(self: "Inserts", other: Union[Stack, "Inserts"]) -> Stack:
        if isinstance(other, Stack):
            newstack = Array._get_stack_in_cache(other.ID)
            newstack = [self.ID] + newstack
        else:
            newstack = [self.ID, other.ID]
        return Stack(newstack)

    @property
    def top(self: "Inserts") -> np.ndarray:
        return self[0]

    @property
    def bot(self: "Inserts") -> np.ndarray:
        return self[1]
