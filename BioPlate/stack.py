from collections import OrderedDict

import numpy as np

from BioPlate.array import BioPlateArray
from BioPlate.manipulation import BioPlateManipulation


class BioPlateStack(BioPlateManipulation):
    """
   {id_stack : [id_plate1, id_plate2]}
   """

    def __init__(self, ID_list):
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

    def __repr__(self):
        BioPlates = [self[i] for i in range(len(self))]
        return str(np.array(BioPlates))

    def __getitem__(self, plate_index):
        return BioPlateArray._get_plate_in_stack(self.ID, plate_index)

    def __setitem__(self, index, value):
        self[index[0]][index[1:]] = value

    def __len__(self):
        return len(BioPlateArray._get_stack_in_cache(self.ID))

    def __add__(self, other):
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

    def change_args(func):
        def wrapper(self, *args, **kwargs):
            bioplate = self[args[0]]
            if len(bioplate.shape) == 2:
                *args, = args[1:]
                return func(self, bioplate, *args, **kwargs)
            else:
                position, *args = args[1:]
                # t =  {"top" : 0, "bot" : 1}
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
