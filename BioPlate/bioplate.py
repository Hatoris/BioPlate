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
from BioPlate.plate import BioPlatePlate
from BioPlate.inserts import BioPlateInserts
from BioPlate.stack import BioPlateStack


@overload
def BioPlate(
    column: int,
    row: int,
    inserts: bool = True,
) -> BioPlateInserts:  # pragma: no cover
    pass

@overload
def BioPlate(
    column: int,
    row: int,
    inserts: bool = False,
) -> BioPlatePlate:  # pragma: no cover
    pass

@overload
def BioPlate(
    nb: int,
    column: int,
    row: int,
    inserts: bool = False,
) -> BioPlateStack:  # pragma: no cover
    pass

@overload
def BioPlate(
    nb: int,
    column: int,
    row: int,
    inserts: bool = True,
) -> BioPlateStack:  # pragma: no cover
    pass

@overload
def BioPlate(
    args: Dict,
    inserts: bool = False,
) -> Union[BioPlatePlate, BioPlateInserts, BioPlateStack]:  # pragma: no cover
    pass

def BioPlate(*args, **kwargs):
    """
    Entry point to create plate object.
    Parameters
    ------------------
    number_of_plate : int, optional
        number of plate to create in a stack
     column: int
         number of column in one plate
     row: int
         number of row in one plate
      plate_history_id : Dict
          id of plate
       inserts : bool, optional
           if plate objwct is an inserts
      Return
      -----------
      plate object
    """
    if len(args) == 2 or isinstance(args[0], dict):
        if kwargs.get("inserts", False):
            return BioPlateInserts(*args, **kwargs)
        else:
            return BioPlatePlate(*args, **kwargs)
    elif len(args) == 3:
        ID_list = []
        nb_plates, *nargs = args
        for nb_plate in range(nb_plates):
            if kwargs.get("inserts", False):
                plate = BioPlateInserts(*nargs, **kwargs)
            else:
                plate = BioPlatePlate(*nargs, **kwargs)
            ID_list.append(id(plate))
        return BioPlateStack(ID_list)

