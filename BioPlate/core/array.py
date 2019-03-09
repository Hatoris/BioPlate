from typing import (
    Dict,
    List,
    Tuple,
    Union,
    overload,
)

from string import ascii_uppercase

import numpy as np

from BioPlate.database.plate_db import PlateDB
from BioPlate.core.matrix import BioPlateMatrix
import BioPlate.core.utilitis as bpu
from BioPlate.core.manipulation import BioPlateManipulation


class Array(np.ndarray, BioPlateManipulation):
    """ 
    Array is core based application, this class is the only one to inerit from np.ndarray.
    This class return a np.array format properly for BioPlate or Inserts.
    A row is symbolise by it's letter, a column by a number.
    """

    _PLATE_CACHE: Dict[
        int, np.ndarray
    ] = {}  # contain id as key and np.array plate as value

    def __new__(cls, *args, **kwargs) -> np.ndarray:
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        if kwargs.get("inserts", False):
            bp = Array.bioplatearray(*args, **kwargs)
            BioPlate = np.array([bp, bp]).view(cls)
        else:
            BioPlate = Array.bioplatearray(*args, **kwargs).view(cls)
        ID = id(BioPlate)
        Array._add_plate_in_cache(ID, BioPlate)
        return Array._get_plate_in_cache(ID)

    def __getitem__(
        self, index: Tuple[Union[int, slice], Union[int, slice], int, str]
    ) -> np.ndarray:
        if isinstance(index, str):
            well = BioPlateMatrix(index)
            return self[well.row, well.column]
        return super(Array, self).__getitem__(index)

    def __setitem__(
        self,
        index: Tuple[Union[int, slice], Union[int, slice]],
        value: Union[List[int], List[str], int, str],
    ) -> None:
        if isinstance(index, str):
            self.set(index, value)
        else:
            super(Array, self).__setitem__(index, value)

    @overload
    def bioplatearray(
        *args: int, **kwargs: str
    ) -> np.ndarray:  # pragma: no cover
        pass

    @overload
    def bioplatearray(
        *args: Dict, **kwargs: str
    ) -> np.ndarray:  # pragma: no cover
        pass

    def bioplatearray(*args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        if isinstance(args[0], list): #used by stack 
            return args[0]
        columns, rows = Array.get_columns_rows(*args, **kwargs)
        return Array.bio_plate_array(columns, rows)

    @overload
    def get_columns_rows(
        *args: int, **kwargs: str
    ) -> Tuple[int, int]:  # pragma: no cover
        pass

    @overload
    def get_columns_rows(
        *args: Union[
            Dict[str, int], Dict[str, str], Dict[str, List[int]], Dict[str, List[str]]
        ],
        **kwargs: str,
    ) -> Tuple[int, int]:  # pragma: no cover
        pass

    def get_columns_rows(*args, **kwargs):
        """
        use to get columns and rows from database call or directly from args.
        
        
        Parameters
        -------------------      
         *args int: 
             number of columns AND number of row
          *args dict:
               dict with key, value for database research
         
         Returns
         -------------
        int, int
            columns, rows of the given args
        
        Raises
        -----------
        AttributeError
            if args and kwargs pass can not be used to return columns and rows value
        
        """
        dict_in = isinstance(args[0], dict)
        all_int = all(isinstance(arg, int) for arg in args)
        if dict_in:
            return Array.get_column_row_from_db(args[0],  **kwargs)
        elif all_int:
            columns, rows = args
            return columns, rows
        raise AttributeError(
                "You should call by passing column, row or {'key' : 'value'} of PlateDB"
            )

    def get_column_row_from_db(dict_infos, **kwargs):
        db_name = kwargs.get("db_name", False)
        try:
            if db_name:
                pdb = PlateDB(db_name=db_name)
            else:
                pdb = PlateDB()
            key, value = list(*dict_infos.items())
            plate = pdb.get_one_plate(str(value), key=str(key))
            return plate.numColumns, plate.numRows
        except AttributeError:
            raise AttributeError(f"invalid format : {dict_infos}")

    def bio_plate_array(columns: int, rows: int) -> np.ndarray:
        """
            Create a representation of biological plate from a given number of columns and rows value.
            
            Parameters
            --------------------          
            columns int:
                number of columns in the plate representation
             rows int:
                 number of rows in the plate representation 
            
            Returns
            -------------
            np.ndarray
                the np.array have a shape of rows+1, columns+1 to feat the header in it.        Datatype inside the returned np.array is U100 in order to get mixed value of str and int.
            
            Exemples
            ----------------
            >>>print(Array.bio_plate_array(3, 2))
            [ [', '1', '2', '3']
              ['A', '', '', '']
              ['B', '', '', '']
              ['C', '', '', ''] ]
            """
        letter = bpu._LETTER[0:rows]
        rows += 1
        columns += 1
        BParray = np.zeros([rows, columns], dtype="U100")
        BParray[0,1:] = np.arange(1, columns)
        BParray[1 : rows, 0] = letter
        return BParray

    def _get_plate_in_cache(plate_id: int) -> np.ndarray:
        """
       return a plate (np.ndarray) for a given plate_id
       
       Parameters
       ---------------------
       plate_id : int
           id of plate obtain by id(plate)
           
       Returns
       --------------
       np.ndarray of given id
       
       Exemples
       -----------------
       >>> from BioPlate import BioPlate
       >>> from BioPlate.array import Array
       >>> plate = BioPlate(12, 8)
       >>> same_plate = Array._get_plate_in_cache(id(plate))
       >>> id(plate) == id(same_plate)
       True
       """
        try:
            return Array._PLATE_CACHE[plate_id]
        except KeyError:
            raise KeyError(f"plate {plate_id} is not in plate cache")

    def _get_stack_in_cache(stack_id: int) -> List[int]:
        """
        return a list of plate id for a given stack_id
       
       Parameters
       ---------------------
       stack_id : int
           id of stack obtain by id(stack)
           
       Returns
       --------------
       List_of_plate_id : list
           list of plate id in stack object
       
       Exemples
       -----------------
       >>> from BioPlate import BioPlate
       >>> from BioPlate.array import Array
       >>> stack = BioPlate(2, 12, 8)
       >>> Array._get_stack_in_cache(id(stack))
       [4356278905, 4356789241]
       """
        try:
            return Array._PLATE_CACHE[stack_id]
        except KeyError:
            raise KeyError(f"stack {stack_id} is not in stack cache")

    def _get_plate_in_stack(stack_id : int, plate_index : int) -> np.ndarray:
        """
        return a plate (np.ndarray) for a given stack_id, and plate_index in stack
       
       Parameters
       ---------------------
       stack_id : int
           id of stack obtain by id(stack)
       plate_index : int
           index of plate in the stack
           
       Returns
       --------------
       plate : np.ndarray
           plate object
       
       Exemples
       -----------------
       >>> from BioPlate import BioPlate
       >>> from BioPlate.array import Array
       >>> stack = BioPlate(2, 12, 8)
       >>> Array._get_plate_in_stack(id(stack), 0)
       [[ '' , 1, 2, 3 ..., 12]
        ['A', '' , ...]
        ...
       """
        try:
            plate_id = Array._get_stack_in_cache(stack_id)[plate_index]
            return Array._get_plate_in_cache(plate_id)
        except KeyError:
            raise KeyError(f"object {stack_id} is not in cache")
        except IndexError:
            raise IndexError(f"index {plate_index} is not in stack {stack_id}")

    def _merge_stack(stack1_id: int, stack2_id: int) -> List[int]:
        """
        return a list of merged id from to stack_id
       
       Parameters
       ---------------------
       stack1_id : int
           id of stack obtain by id(stack1)
        stack2_id : int
           id of stack obtain by id(stack2) 
           
       Returns
       --------------
       List_of_merge_stack_id : list
           list of plate id from stack1 and stack2 object
       
       Exemples
       -----------------
       >>> from BioPlate import BioPlate
       >>> from BioPlate.array import Array
       >>> stack1 = BioPlate(2, 12, 8)
       >>> stack2 = BioPlate(2, 12, 8)
       >>> Array._merge_stack(id(stack1), id(stack2))
       [4356278905, 4356789241, 3456890234, 2346789120]
       """
        try:
            newstack = (
                Array._PLATE_CACHE[stack1_id]
                + Array._PLATE_CACHE[stack2_id]
            )
            return newstack
        except KeyError:
            raise KeyError(
                f"Either stack1_id {stack1_id} or stack2_id {stack2_id} are not in cache"
            )

    def _add_stack_to_cache(stack_id: int, id_list: List[int]) -> None:
        """
        add list of id to stack cache
       
       Parameters
       ---------------------
       stack1_id : int
           id of stack obtain by id(stack1)
        id_list: list
           List of plate id 
           
       Returns
       --------------
      None
       
       Exemples
       -----------------
       >>> from BioPlate import BioPlate
       >>> from BioPlate.array import Array
       >>> plate1 = BioPlate(12, 8)
       >>> plate2 = BioPlate(12, 8)
       >>> stack = [id(plate1), id(plate2)]
       >>> Array._add_stack_to_cache(123, stack)
       >>>
        """
        #Array._add_plate_in_cache(stack_id, id_list)
        Array._PLATE_CACHE[stack_id] = id_list
        return None

    def _add_plate_in_cache(plate_id: int, plate: np.ndarray) -> None:
        """
        add plate (np.ndarray) in cache
       
       Parameters
       ---------------------
       plate_id : int
           id of plate obtain by id(stack1)
        plate: np.ndarray
           plate object
           
       Returns
       --------------
      None
       
       Exemples
       -----------------
       >>> import numpy as np
       >>> from BioPlate.array import Array
       >>> plate = np.arange(117).reshape(13,9)
       >>> Array._add_plate_in_cache(123, plate)
       >>>
       """
        if plate_id not in Array._PLATE_CACHE:
            Array._PLATE_CACHE[plate_id] = plate
        return None
