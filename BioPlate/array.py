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
from BioPlate.matrix import BioPlateMatrix
import BioPlate.utilitis as bpu


class Array(np.ndarray):
    """ 
    Array is core based application, this class is the only one to inerit from np.ndarray.
    This class return a np.array format properly for BioPlate or Inserts.
    A row is symbolise by it's letter, a column by a number.
    """

    _PLATE_CACHE: Dict[
        int, np.ndarray
    ] = {}  # contain id as key and np.array plate as value
    _STACK_CACHE: Dict[
        int, List[int]
    ] = {}  # contain id of stak plate as key and list of unique plate bioplatestack cache

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
        if ID not in Array._PLATE_CACHE:
            Array._PLATE_CACHE[ID] = BioPlate
        return Array._PLATE_CACHE[ID]

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
            well = BioPlateMatrix(index)
            if isinstance(value, list):
                plate_shape = self[well.row, well.column].shape
                len_plate_shape = len(plate_shape)
                if len_plate_shape > 1:
                    if well.pos == "R":
                        resh_val = np.reshape(value, (plate_shape[0], 1))
                    else:
                        resh_val = value
                    self[well.row, well.column] = resh_val
                    return
                else:
                    self[well.row, well.column][: len(value)] = value
                    return
            else:
                self[well.row, well.column] = value
                return
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
        try:
            if isinstance(args[0], list):
                return args[0]
            elif len(args) == 2 or isinstance(args[0], dict):
                columns, rows = Array.get_columns_rows(*args, **kwargs)
                if isinstance(columns, int) and isinstance(rows, int):
                    return Array.bio_plate_array(columns, rows)
                else:
                    raise ValueError
        except ValueError:
            raise ValueError(f"Something wrong with {args}")

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
            if args and kwargs pass can be used to return columns and rows value
        
        """
        dict_in = isinstance(args[0], dict)
        if len(args) == 2 and not dict_in:
            columns, rows = args
            plate = None
        elif (len(args) == 1 or len(args) == 2) and dict_in:
            try:
                if "db_name" in kwargs:
                    pdb = PlateDB(db_name=kwargs["db_name"])
                else:
                    pdb = PlateDB()
                pair = list(args[0].items())
                k, arg = pair[0]
                plate = pdb.get_one_plate(str(arg), key=str(k))
                columns = plate.numColumns
                rows = plate.numRows
            except AttributeError:
                raise AttributeError(f"invalid format : {dict}")
        elif len(args) == 1:
            return (0,)
        else:
            raise AttributeError(
                "You should call by passing column, row or {'key' : 'value'} of PlateDB"
            )
        return columns, rows

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
        BParray = np.zeros([rows + 1, columns + 1], dtype="U100")
        BParray[0] = np.arange(columns + 1)
        BParray[1 : rows + 1, 0] = np.array(list(ascii_uppercase))[0:rows]
        BParray[0, 0] = " "
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
            return Array._STACK_CACHE[stack_id]
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
                Array._STACK_CACHE[stack1_id]
                + Array._STACK_CACHE[stack2_id]
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
        Array._STACK_CACHE[stack_id] = id_list
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

    def _get_list_id_of_stack(stack_object: "Array") -> List[int]:
        """
        Get a list of plate id in stack 
       
       Parameters
       ---------------------
       stack_object: Stack
           Stack object
           
       Returns
       --------------
       id_list
       
       Exemples
       -----------------
       >>> from BioPlate import BioPlate
       >>> from BioPlate.array import Array
       >>> stack = BioPlate(2, 12, 8)
       >>> Array._get_list_id_of_stack(stack)
        [4356278905, 4356789241]
       """
        if stack_object.name == "Stack":
            id_list = []
            for plate in stack_object:
                plate_id = id(plate)
                id_list.append(plate_id)
            return id_list
        else:
            raise ValueError("plate_object is not a stack")
