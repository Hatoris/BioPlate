import numpy as np
from BioPlate.database.plate_db import PlateDB
import BioPlate.utilitis as bpu #import _LETTER, dimension
from time import time, sleep


class BioPlateArray(np.ndarray):
    """A row is symbolise by it's letter, a column by a number"""    
    
    _PLATE_CACHE = {} # contain id as key and np.array plate as value 
    _STACK_CACHE = {} # contain id of stak plate as key and list of unique plate bioplatestack cache
    _CACHE_BPA = {} # contain plate 
    
    def __new__(cls, *args, **kwargs):
        BioPlate =   BioPlateArray.bioplatearray(*args, **kwargs).view(cls)
        ID = id(BioPlate)
        if ID not in BioPlateArray._PLATE_CACHE:
               BioPlateArray._PLATE_CACHE[ID] = BioPlate
        return BioPlateArray._PLATE_CACHE[ID]

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
            BParray[0] = np.arange( columns+1)
            BParray[1:rows+1, 0] = bpu._LETTER[0:rows]
            BParray[0,0] = ' '
            return BParray
    
    def _bio_plate_array(columns, rows):
        key = (columns, rows)
        if key not in BioPlateArray._CACHE_BPA:
            BParray = BioPlateArray._bio_plate_array(columns, rows)
            BioPlateArray._CACHE_BPA[key] = BParray
        return  BioPlateArray._CACHE_BPA[key]
            
    
    def BioPlate_parameters(BioPlate):
        BioPlate_dimension = bpu.dimension(BioPlate)
        BioPlate_shape = BioPlate.shape
        if BioPlate_dimension:
            stack, rows, columns = BioPlate_shape
        else:
            stack = 0
            columns, rows = BioPlate_shape
        return BioPlate_dimension, stack, rows - 1, columns - 1


    def _get_plate_in_cache(ID):
       """
       return a plate for a given ID 
       """
       try:
          return BioPlateArray._PLATE_CACHE[ID]
       except KeyError:
          raise KeyError(f"plate {ID} is not in plate cache")
          
    def _get_stack_in_cache(ID):
       """
       return a plate for a given ID 
       """
       try:
          return BioPlateArray._STACK_CACHE[ID]
       except KeyError:
          raise KeyError(f"plate {ID} is not in stack cache")
          
    def _get_plate_in_stack(stack_ID, plate_index):
          ID = BioPlateArray._get_stack_in_cache(stack_ID)[plate_index]
          return BioPlateArray._get_plate_in_cache(ID)
          
    def _merge_stack(stack1_ID, stack2_ID):
         newstack = BioPlateArray._STACK_CACHE[stack1_ID] + BioPlateArray._STACK_CACHE[stack2_ID]
         return newstack
          
          
    def _add_stack_to_cache(stack_ID, ID_list):
        BioPlateArray._STACK_CACHE[stack_ID] = ID_list
        
    def _add_plate_in_cache(ID, BioPlate):
         if ID not in BioPlateArray._PLATE_CACHE:
               BioPlateArray._PLATE_CACHE[ID] = BioPlate
        
   
    def _get_list_id_of_stack(plate_object):
        if bpu.dimension(plate_object):
                ID_list = []
                for plate in plate_object:
                    iD= id(plate)
                    ID_list.append(iD)
                return ID_list
        else:
            raise ValueError("plate_object is not a stack")

if __name__ == "__main__":
    t0 = time()
    print(BioPlateArray.bio_plate_array(12,8))
    t1 = time()
    print(BioPlateArray.bio_plate_array(12,8))
    t2 = time()
    print(f"call 1 {t1 - t0}, call 2 {t2 - t1}")