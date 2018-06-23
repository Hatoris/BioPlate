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

from BioPlate.array import BioPlateArray
from BioPlate.manipulation import BioPlateManipulation


class BioPlateStack(BioPlateManipulation):
    """
   {id_stack : [id_plate1, id_plate2]}
   """

    def __init__(self: "BioPlateStack", ID_list: List[int]) -> None:
        self.ID = id(self)
        if isinstance(ID_list[0], int):
            BioPlateArray._add_stack_to_cache(self.ID, ID_list)
        else:
            new_ID_list = []
            for BP in ID_list:
                ID = id(BP)
                new_ID_list.append(ID)
                BioPlateArray._add_plate_in_cache(ID, BP)
            BioPlateArray._add_stack_to_cache(self.ID, new_ID_list)

    def __repr__(self: "BioPlateStack") -> str:
        BioPlates = [self[i] for i in range(len(self))]
        return str(np.array(BioPlates))

    def __getitem__(
        self: "BioPlateStack",
        index: Union[slice, int, Tuple[int, str], Tuple[int, str, str]],
    ) -> np.ndarray:
        if isinstance(index, int):
            return BioPlateArray._get_plate_in_stack(self.ID, index)
        if isinstance(index, tuple):
            plt = BioPlateArray._get_plate_in_stack(self.ID, index[0])
            if isinstance(index[1], str):
                if plt.name == "BioPlateInserts":
                    return plt[index[1], index[2]]
                return plt[index[1]]
            else:
                return plt[index[1:]]

    def __setitem__(
        self: "BioPlateStack",
        index: Union[Tuple[int, str], Tuple[int, str, str]],
        value: Union[List[int], List[str], int, str],
    ) -> None:
        if isinstance(index[1], str):
            if self[index[0]].name == "BioPlateInserts":
                self[index[0]][index[1], index[2]] = value
                return
            self[index[0]][index[1]] = value
            return
        else:
            self[index[0]][index[1:]] = value
            return

    def __len__(self: "BioPlateStack") -> int:
        return len(BioPlateArray._get_stack_in_cache(self.ID))

    def __add__(
        self: "BioPlateStack", other: Union["BioPlateStack", BioPlateArray]
    ) -> "BioPlateStack":
        if type(self[0]) == type(other):
            newstack = BioPlateArray._get_stack_in_cache(self.ID)
            if other.ID not in newstack:
                newstack.append(other.ID)
            else:
                raise ValueError(f"{other} already in stack")
        elif type(self) == type(other):
            newstack = BioPlateArray._merge_stack(self.ID, other.ID)
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)

    def change_args(func: Callable) -> Callable:
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
