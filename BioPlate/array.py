from string import ascii_uppercase

import numpy as np

from BioPlate.database.plate_db import PlateDB


class BioPlateArray(np.ndarray):
    """ 
    BioPlateArray is core based application, this class is the only one to inerit from np.ndarray. 
    This class return a np.array format properly for BioPlate or BioPlateInserts. 
    A row is symbolise by it's letter, a column by a number.
    """

    _PLATE_CACHE = {}  # contain id as key and np.array plate as value
    _STACK_CACHE = {}  # contain id of stak plate as key and list of unique plate bioplatestack cache
    _CACHE_BPA = {}  # contain plate

    def __new__(cls, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        if kwargs.get("inserts", False):
            bp = BioPlateArray.bioplatearray(*args, **kwargs)
            BioPlate = np.array([bp, bp]).view(cls)
        else:
            BioPlate = BioPlateArray.bioplatearray(*args, **kwargs).view(cls)
        ID = id(BioPlate)
        if ID not in BioPlateArray._PLATE_CACHE:
            BioPlateArray._PLATE_CACHE[ID] = BioPlate
        return BioPlateArray._PLATE_CACHE[ID]

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
                columns, rows = BioPlateArray.get_columns_rows(*args, **kwargs)
                if isinstance(columns, int) and isinstance(rows, int):
                    return BioPlateArray.bio_plate_array(columns, rows)
                else:
                    raise ValueError
        except ValueError:
            raise ValueError(f"Something wrong with {args}")

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
                raise AttributeError(plate)
        elif len(args) == 1:
            return (0,)
        else:
            raise AttributeError(
                "You should call by passing column, row or {'key' : 'value'} of PlateDB"
            )
        return columns, rows

    def bio_plate_array(columns, rows):
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
            >>>print(BioPlateArray.bio_plate_array(3, 2))
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

    # def _bio_plate_array(columns, rows):
    #     """
    #      Looking cache for np.ndarray with columns, rows as key
    #
    #         Parameters
    #         --------------------
    #         columns int:
    #             number of columns in the plate representation
    #          rows int:
    #              number of rows in the plate representation
    #
    #         Returns
    #         -------------
    #         np.ndarray
    #            np.ndarray from cache
    #
    #     """
    #     key = (columns, rows)
    #     if key not in BioPlateArray._CACHE_BPA:
    #         BParray = BioPlateArray._bio_plate_array(columns, rows)
    #         BioPlateArray._CACHE_BPA[key] = BParray
    #     return  BioPlateArray._CACHE_BPA[key]
    
    @staticmethod
    def _get_plate_in_cache(plate_id):
        """
       return a plate for a given plate_id 
       """
        try:
            return BioPlateArray._PLATE_CACHE[plate_id]
        except KeyError:
            raise KeyError(f"plate {plate_id} is not in plate cache")

    def _get_stack_in_cache(plate_id):
        """
       return a plate for a given ID 
       """
        try:
            return BioPlateArray._STACK_CACHE[plate_id]
        except KeyError:
            raise KeyError(f"plate {plate_id} is not in stack cache")

    def _get_plate_in_stack(stack_id, plate_index):
        plate_id = BioPlateArray._get_stack_in_cache(stack_id)[plate_index]
        return BioPlateArray._get_plate_in_cache(plate_id)

    def _merge_stack(stack1_id, stack2_id):
        newstack = (
            BioPlateArray._STACK_CACHE[stack1_id]
            + BioPlateArray._STACK_CACHE[stack2_id]
        )
        return newstack

    def _add_stack_to_cache(stack_id, id_list):
        BioPlateArray._STACK_CACHE[stack_id] = id_list

    def _add_plate_in_cache(plate_id, BioPlate):
        if plate_id not in BioPlateArray._PLATE_CACHE:
            BioPlateArray._PLATE_CACHE[plate_id] = BioPlate

    def _get_list_id_of_stack(plate_object):
        if plate_object.name == "BioPlateStack":
            id_list = []
            for plate in plate_object:
                plate_id = id(plate)
                id_list.append(plate_id)
            return id_list
        else:
            raise ValueError("plate_object is not a stack")
