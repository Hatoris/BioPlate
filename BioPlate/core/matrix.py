import re
from functools import lru_cache
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

import numpy as np

import BioPlate.core.utilitis as bpu

   
@lru_cache(maxsize=128)
def  well_to_index(well : str) -> bpu.EL:
    """
    from a raw string representing well, convert it to an index for slicing BioPlate object
    
    Parameters
    -------------------
    well : str
        A human representation of well (eg: A-B[2-8])
        
    Returns
    -------------
    Coordinate : named tuple
        return a name tuple with following informations
        - position : row or column
        - row slicing aka first dimension of numpy array
        - column slicing aka second dimension of numpy array
    """
    is_zero(well)
    left, right = split_well_infos(well)
    pos = position(left)
    row, column, pos = index_formater(left, right, pos)
    return index(pos, row, column)

def position(infos: str) -> str:
    """
    return R or C based on infos first elements, if it is a digit return C for column, otherwise R for row
    """
    if infos[0].isdigit():
        return "C"
    return "R"    

def index_formater(left : str, right : str, pos : str) -> Tuple[Union[int, slice], Union[int, slice]]:
    """
    evaluate if right is None, if true well information represent an entire row or column. Else futher comparaison should be performed
    """
    if right is None:
        return entire_row_column(left, pos)
    return  one_well(left, right, pos)

def entire_row_column(left : str, pos : str) -> Union[Tuple[int, slice, str], Tuple[slice, int, str]]:
    """
    return index for an entire column or row
    
    """
    if pos == "R":
        return row_index(left), slice(1, None), pos 
    return slice(1, None), column_index(left), pos

def row_index(infos : str) -> Union[str, slice]:
    if len(infos) == 1:
        row = convert_letter_to_index(infos)
        return row
    start, stop = split_multi_value(infos)
    return slice(start, stop, 1)
        
def column_index(infos : str) -> Union[int, slice]:
    """
    return ind3x for column.
    
    Parameters
    -------------------
    infos : str
        a string with column value eg : "1", "1-9"
        
    Returns 
    -----------
    index : int, slice
        Int or slice of column
    """
    try:
        column = int(infos)
        return column
    except ValueError:
        start, stop = split_multi_value(infos)
        return slice(start, stop, 1)

def one_well(left : str, right: str, pos : str) -> Tuple[int, int, str]:
    if pos == "R":
        row = row_index(left)
        column = column_index(right)
    else:
        row = row_index(right)
        column = column_index(left)
    if len(left) == 1 and len(right) == 1:
        pos = "W"
    return row, column, pos
    
def split_well_infos(well: str) -> Tuple[str, str]:
    """
        split string well on left and right part.
        eg :
            'A12' => ('A', '12')
            'B[2-8]' => ('B', '2-8')
            '2-9[A-D]' => ('2-9', 'A-D')
    """
    left : str
    right : str
    try:
        left, right = bpu._FIND_LEFT_RIGHT .findall(well)
    except ValueError:
        left, right = well, None
    return left, right

def split_multi_value(multi : str ) -> Tuple[str, str]:
    try:
        start, stop = map(int, sorted(bpu._SPECIAL_CHAR.split(multi), key=float))
    except ValueError:
        start, stop = map(convert_letter_to_index, sorted(bpu._SPECIAL_CHAR.split(multi)))
    return start, stop + 1 # +1 is mandatory to slect the right position and avoid rembering that list slicing do not include the last element

def convert_letter_to_index(row_letter: str) -> int:
    """
        get index for a given letter (eg : C)
        
        :param row_letter: C => letter of a row
        :return: 3 => index of row C in plate.array
    """
    return np.searchsorted(bpu._LETTER, row_letter) + 1
    
def index(pos : str, row: Union[int, slice], column : Union[int, slice]) -> bpu.EL:
    """
    Return a namedtuple with informations to isolate or slice bioplate
    """
    return bpu.EL(pos, row, column)
   
def is_zero(well: str) -> Optional[str]:
    """
    test if a well infos contain reference to column 0.
    """
    if bool(bpu._FIND_ZERO.search(well)):
        raise ValueError(f"well = {well} is not allowed, column 0 is forbiden")   
