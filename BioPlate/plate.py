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
    ClassVar,
)

from collections import OrderedDict

from BioPlate.array import BioPlateArray
from BioPlate.manipulation import BioPlateManipulation
from BioPlate.stack import BioPlateStack


class BioPlatePlate(BioPlateArray, BioPlateManipulation):
    """
    you can add on it all function of plate
    """

    def __new__(cls, *args, **kwargs):
        return BioPlateArray.__new__(cls, *args, **kwargs)

    def __init__(self: "BioPlatePlate", *args, **kwargs) -> None:
        self.ID: int = id(self)

    def __add__(
        self: "BioPlatePlate", other: Union[BioPlateArray, BioPlateStack]
    ) -> BioPlateStack:
        if isinstance(other, BioPlateStack):
            newstack = BioPlateArray._get_stack_in_cache(other.ID)
            newstack = [self.ID] + newstack
        else:
            newstack = [self.ID, other.ID]
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)