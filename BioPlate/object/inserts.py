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

    @overload
    def __setitem__(
        self: "Inserts",
        index: Tuple[Union[int, slice], Union[int, slice]],
        value: Union[List[int], List[str], int, str],
    ) -> None:  # pragma: no cover
        pass

    @overload
    def __setitem__(
        self: "Inserts",
        index: Union[str, Tuple[int, slice], int],
        value: Union[List[int], List[str], int, str],
    ) -> None:  # pragma: no cover
        pass

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            if any(isinstance(i, str) for i in index):
                ind = self._ind.get(index[0])
                plt = self[ind]
                if isinstance(index[1], str):
                    well = BioPlateMatrix(index[1])
                    plt[index[1]] = value
                    return
        super(Inserts, self).__setitem__(index, value)

    @property
    def top(self: "Inserts") -> np.ndarray:
        return self[0]

    @property
    def bot(self: "Inserts") -> np.ndarray:
        return self[1]

    def force_position(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            if len(self.shape) > 2:
                raise ValueError(
                    "You didn't select a part of the plate, either top or bot'"
                )
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @force_position
    def set(self, *args, **kwargs):
        super().set(*args, **kwargs)
        return self

    @force_position
    def get(self, *args):
        return super().get(*args)
