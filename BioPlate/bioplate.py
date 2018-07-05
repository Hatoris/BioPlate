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

from BioPlate.plate import Plate
from BioPlate.inserts import Inserts
from BioPlate.stack import Stack


@overload
def BioPlate(
    nb: int,
    column: int,
    row: int,
    inserts: bool = False,
) -> Stack:  # pragma: no cover
    pass

@overload
def BioPlate(
    nb: int,
    column: int,
    row: int,
    inserts: bool = True,
) -> Stack:  # pragma: no cover
    pass

@overload
def BioPlate(
    args: Dict,
    inserts: bool = False,
) -> Union[Plate, Inserts, Stack]:  # pragma: no cover
    pass
    
@overload
def BioPlate(
    column: int,
    row: int,
    inserts: bool = False,
) -> Plate:  # pragma: no cover
    pass    

@overload
def BioPlate(
    column: int,
    row: int,
    inserts: bool = True,
) -> Inserts:  # pragma: no cover
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
            return Inserts(*args, **kwargs)
        else:
            return Plate(*args, **kwargs)
    elif len(args) == 3:
        ID_list = []
        nb_plates, *nargs = args
        for nb_plate in range(nb_plates):
            if kwargs.get("inserts", False):
                plate = Inserts(*nargs, **kwargs)
            else:
                plate = Plate(*nargs, **kwargs)
            ID_list.append(id(plate))
        return Stack(ID_list)

