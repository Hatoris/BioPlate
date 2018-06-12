from collections import OrderedDict

from BioPlate.array import BioPlateArray
from BioPlate.manipulation import BioPlateManipulation
from BioPlate.stack import BioPlateStack


class BioPlateInserts(BioPlateArray, BioPlateManipulation):
    def __new__(cls, *args, **kwargs):
        return BioPlateArray.__new__(cls, *args, inserts=True)

    def __init__(self, *args, **kwargs):
        self.ID = id(self)

    def __add__(self, other):
        if isinstance(other, BioPlateStack):
            newstack = BioPlateArray._get_stack_in_cache(other.ID)
            newstack = [self.ID] + newstack
        else:
            newstack = [self.ID, other.ID]
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)

    @property
    def top(self):
        return self[0]

    @property
    def bot(self):
        return self[1]

    def force_position(func):
        def wrapper(self, *args, **kwargs):
            if len(self.shape) > 2:
                raise ValueError(
                    "You didn't select a part of the plate, either top or bot'"
                )
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @force_position
    def set(self, *args):
        super().set(*args)
        return self

    @force_position
    def get(self, *args):
        return super().get(*args)
