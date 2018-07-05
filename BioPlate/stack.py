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

from collections import OrderedDict

import numpy as np

from BioPlate.array import Array
from BioPlate.manipulation import BioPlateManipulation


class Stack(BioPlateManipulation):
    """
   {id_stack : [id_plate1, id_plate2]}
   """

    def __init__(self: "Stack", ID_list: List[int]) -> None:
        self.ID = id(self)
        if isinstance(ID_list[0], int):
            Array._add_stack_to_cache(self.ID, ID_list)
        else:
            new_ID_list = []
            for BP in ID_list:
                ID = id(BP)
                new_ID_list.append(ID)
                Array._add_plate_in_cache(ID, BP)
            Array._add_stack_to_cache(self.ID, new_ID_list)

    def __repr__(self: "Stack") -> str:
        BioPlates = [self[i] for i in range(len(self))]
        return str(np.array(BioPlates))

    def __getitem__(
        self: "Stack",
        index: Union[slice, int, Tuple[int, str], Tuple[int, str, str]],
    ) -> np.ndarray:
        if isinstance(index, int):
            return Array._get_plate_in_stack(self.ID, index)
        if isinstance(index, tuple):
            plt = Array._get_plate_in_stack(self.ID, index[0])
            if isinstance(index[1], str):
                if plt.name == "Inserts":
                    return plt[index[1], index[2]]
                return plt[index[1]]
            else:
                return plt[index[1:]]

    def __setitem__(
        self: "Stack",
        index: Union[Tuple[int, str], Tuple[int, str, str]],
        value: Union[List[int], List[str], int, str],
    ) -> None:
        if isinstance(index[1], str):
            if self[index[0]].name == "Inserts":
                self[index[0]][index[1], index[2]] = value
                return
            self[index[0]][index[1]] = value
            return
        else:
            self[index[0]][index[1:]] = value
            return

    def __len__(self: "Stack") -> int:
        return len(Array._get_stack_in_cache(self.ID))

    def __add__(
        self: "Stack", other: Union["Stack", Array]
    ) -> "Stack":
        if type(self[0]) == type(other):
            newstack = Array._get_stack_in_cache(self.ID)
            if other.ID not in newstack:
                newstack.append(other.ID)
            else:
                raise ValueError(f"{other} already in stack")
        elif type(self) == type(other):
            newstack = Array._merge_stack(self.ID, other.ID)
        newstack = list(OrderedDict.fromkeys(newstack))
        return Stack(newstack)

    def change_args(func: Any):
        def wrapper(self, *args, **kwargs):
            bioplate = self[args[0]]
            if len(bioplate.shape) == 2:
                *args, = args[1:]
                return func(self, bioplate, *args, **kwargs)
            else:
                position, *args = args[1:]
                bioplate = getattr(bioplate, position)
                return func(self, bioplate, *args, **kwargs)
        return wrapper

    @change_args
    def set(self, bioplate, *args, **kwargs):
        bioplate.set(*args, **kwargs)
        return self

    @change_args
    def get(self, bioplate, *args):
        return bioplate.get(*args)
