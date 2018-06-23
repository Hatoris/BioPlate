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
from BioPlate.inserts import BioPlateInserts
from BioPlate.manipulation import BioPlateManipulation
from BioPlate.stack import BioPlateStack


class BioPlate(BioPlateArray, BioPlateManipulation):
    """
    you can add on it all function of plate
    """

    @overload
    def __new__(
        cls: Union["BioPlate", BioPlateArray, BioPlateInserts, BioPlateStack],
        args: int,
        args1: int,
        inserts: bool = True,
    ) -> BioPlateInserts:  # pragma: no cover
        pass

    @overload
    def __new__(
        cls: Union["BioPlate", BioPlateArray, BioPlateInserts, BioPlateStack],
        args: int,
        args1: int,
        inserts: bool = False,
    ) -> BioPlateArray:  # pragma: no cover
        pass

    @overload
    def __new__(
        cls: Union["BioPlate", BioPlateArray, BioPlateInserts, BioPlateStack],
        args: int,
        args1: int,
        args2: int,
        inserts: bool = False,
    ) -> BioPlateStack:  # pragma: no cover
        pass

    @overload
    def __new__(
        cls: Union["BioPlate", BioPlateArray, BioPlateInserts, BioPlateStack],
        args: int,
        args1: int,
        args2: int,
        inserts: bool = True,
    ) -> BioPlateStack:  # pragma: no cover
        pass

    @overload
    def __new__(
        cls: Union["BioPlate", BioPlateArray, BioPlateInserts, BioPlateStack],
        args: Dict,
        inserts: bool = False,
    ) -> BioPlateStack:  # pragma: no cover
        pass

    def __new__(cls, *args, **kwargs):
        if len(args) == 2 or isinstance(args[0], dict):
            if kwargs.get("inserts", False):
                return BioPlateInserts(*args, **kwargs)
            else:
                return BioPlateArray.__new__(cls, *args, **kwargs)
        elif len(args) == 3:
            ID_list = []
            nb_plates, *nargs = args
            for nb_plate in range(nb_plates):
                if kwargs.get("inserts", False):
                    plate = BioPlateInserts(*nargs, **kwargs)
                else:
                    plate = BioPlateArray.__new__(cls, *nargs, **kwargs)
                ID_list.append(id(plate))
            return BioPlateStack(ID_list)

    def __init__(self: "BioPlate", *args, **kwargs) -> None:
        self.ID: int = id(self)

    def __add__(
        self: "BioPlate", other: Union[BioPlateArray, BioPlateStack]
    ) -> BioPlateStack:
        if isinstance(other, BioPlateStack):
            newstack = BioPlateArray._get_stack_in_cache(other.ID)
            newstack = [self.ID] + newstack
        else:
            newstack = [self.ID, other.ID]
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)
