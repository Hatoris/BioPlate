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
import numpy as np 

from BioPlate.core.array import Array
from BioPlate.core.manipulation import BioPlateManipulation
from BioPlate.object.stack import Stack


class Plate(Array, BioPlateManipulation):
    """
    you can add on it all function of plate
    """

    def __new__(cls, *args, **kwargs) -> "Plate":
        return Array.__new__(cls, *args, **kwargs)

    def __init__(self: "Plate", *args, **kwargs) -> None:
        self.ID: int = id(self)

    def __add__(
        self: "Plate", other: Union[Array, Stack]
    ) -> Stack:
        if isinstance(other, Stack):
            newstack = Array._get_stack_in_cache(other.ID)
            newstack = [self.ID] + newstack
        else:
            newstack = [self.ID, other.ID]
        return Stack(newstack)
        