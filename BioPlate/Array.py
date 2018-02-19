import numpy as np

from string import ascii_uppercase
#from functools import lru_cache
from BioPlate.database.plate_db import PlateDB
from BioPlate.utilitis import _LETTER, dimension


class BioPlateArray(np.ndarray):
    """A row is symbolise by it's letter, a column by a number"""    
    
    _BIOPLATE_CACHE = {} # contain id as key and np.array plate as value 
    _STACK_ID = {} # contain id of stak plate as key and list of unique plate bioplatestack cache
    
    def __new__(cls, *args, **kwargs):
        BioPlate =   BioPlateArray.bioplatearray(*args, **kwargs).view(cls)
        ID = id(BioPlate)
        if ID not in BioPlateArray._BIOPLATE_CACHE:
               BioPlateArray._BIOPLATE_CACHE[ID] = BioPlate
        return BioPlateArray._BIOPLATE_CACHE[ID]

    def bioplatearray(*args, **kwargs):
        try:
    	    columns, rows = BioPlateArray.get_columns_rows(*args, **kwargs)
    	    if isinstance(columns, int) and isinstance(rows, int):
    	        return BioPlateArray.bio_plate_array(columns, rows)
    	    else:
    	        raise ValueError
        except ValueError:
            return args[0]
    	
    	
    
    def get_columns_rows(*args, **kwargs):
        """
        use to get columns and rows
        
        :param int args1: number of columns
        :param int args2: number of rows
        :param dict args3: key value in PlateDB
        :return: columns, rows
        
        """
        dict_in = isinstance(args[0], dict)
        if len(args) == 2 and not dict_in:
            columns, rows = args
            plate = None
        elif (len(args) == 1 or len(args) == 2) and dict_in :
    	    try:
    	        if 'db_name' in kwargs:
    	            pdb = PlateDB( db_name=kwargs['db_name'])
    	        else :
    	            pdb = PlateDB()
    	        pair = list(args[0].items())
    	        k , arg = pair[0]
    	        plate = pdb.get_one_plate(str(arg), key=str(k))
    	        columns = plate.numColumns
    	        rows = plate.numRows
    	    except AttributeError:
    		    raise AttributeError(plate)
        elif len(args) == 1:
    		    return (0,)
        else:
            raise AttributeError("You should call by passing column, row or {'key' : 'value'} of PlateDB")
        return columns, rows
    
    
    def bio_plate_array(columns, rows):
            """
            get a numpy.array representation of a plate in dtype='U40' (eg : 6 wells plate)
            
            :return: np.array([[0, 1, 2, 3], [A, 0, 0, 0], [B, 0, 0, 0]])
            """
            BParray = np.zeros([rows + 1, columns + 1], dtype='U40')
            BParray[0] = np.array([x for x in range(columns + 1)])
            for i in range(rows):
                z = i + 1
                BParray[z][0] = _LETTER[i]
            BParray[0][0] = ' '
            return BParray
    
    
    def BioPlate_parameters(BioPlate):
        BioPlate_dimension = dimension(BioPlate)
        BioPlate_shape = BioPlate.shape
        if BioPlate_dimension:
            stack, rows, columns = BioPlate_shape
        else:
            stack = 0
            columns, rows = BioPlate_shape
        return BioPlate_dimension, stack, rows - 1, columns - 1


    @classmethod
    def _get_bioplate_in_cache(cls, ID):
       """
       return a plate for a given ID 
       """
       try:
          return BioPlateArray._BIOPLATE_CACHE[ID]
       except KeyError:
          raise KeyError(f"plate {ID} is not in cache")
          
    @classmethod
    def _add_plate_to_stack(multi_plate_ID, ID_list):
        BioPlateArray._STACK_ID[stack_plate_ID] = ID_list
        
    @classmethod
    def _add_plate_in_cache(ID, BioPlate):
         if ID not in BioPlateArray._BIOPLATE_CACHE:
               BioPlateArray._BIOPLATE_CACHE[ID] = BioPlate
        
    @classmethod
    def _get_list_id_of_stack(plate_object):
        if dimension(plate_object):
                ID_list = []
                for plate in plate_object:
                    iD= id(plate)
                    ID_list.append(iD)
                return ID_list
        else:
            raise ValueError("plate_object is not a stack")