import time
import numpy as np

from tabulate import tabulate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.utilitis import dimension, _LETTER
from BioPlate.Array import BioPlateArray
from BioPlate.Manipulation import BioPlateManipulation



class CPlate(np.ndarray):
    """A row is symbolise by it's letter, a column by a number"""    
    
    _BIOPLATE_CACHE = {} # contain id as key and np.array plate as value 
    _STACK_ID = {} # contain id of stak plate as key and list of unique plate bioplatestack cache
    
    def __new__(cls, *args, **kwargs):
        BioPlate = BioPlateArray(*args, **kwargs).view(cls)
        ID = id(BioPlate)
        if ID not in CPlate._BIOPLATE_CACHE:
               CPlate._BIOPLATE_CACHE[ID] = BioPlate
        return CPlate._BIOPLATE_CACHE[ID]
       
    @classmethod
    def _get_bioplate_in_cache(cls, ID):
       """
       return a plate for a given ID 
       """
       try:
          return CPlate._BIOPLATE_CACHE[ID]
       except KeyError:
          raise KeyError(f"plate {ID} is not in cache")
          
    @classmethod
    def _add_plate_to_stack(multi_plate_ID, ID_list):
        CPlate._STACK_ID[stack_plate_ID] = ID_list
        
    @classmethod
    def _add_plate_in_cache(ID, BioPlate):
         if ID not in CPlate._BIOPLATE_CACHE:
               CPlate._BIOPLATE_CACHE[ID] = BioPlate
        
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

        
                
class manipulatePlate:
    
    def __init__(self):
        pass
    
    def modif(self, *args):
       plate, col, row, value = self._args_eval(*args)
       if plate is not None:
              self[plate, col, row] = value
       else:
              self[col, row] = value
       
    def _args_eval(self, *args):
        if len(args) == 3:
             col, row, value = args
             plate = None
        elif len(args) == 4:
              plate, col, row, value = args
        return plate, col, row, value
    
                                 
                                        

class BioPlate(BioPlateArray, BioPlateManipulation):
    """
    you can add on it all function of plate
    """
    
    def  __init__(self, *args, **kwargs):
        self.ID = id(self)
       
    def __add__(self, other):
        dims = dimension(self)
        dimo = dimension(other)
        id_list = []
        if dims and dimo:
            pass
        id_list = [self.ID, other.ID]
        return BioPlateStack(id_list)    
              
    def add_value(self, *args):
         super().add_value(*args)
                    
                            
class BioPlateStack(BioPlateManipulation):
   """
   {id_stack : [id_plate1, id_plate2]}
   """
    
   _PLATE_STACK = {}
   
   def __init__(self, ID_list):
       self.ID = id(self)
       BioPlateStack._PLATE_STACK[self.ID] = ID_list
       BioPlateArray._STACK_ID[self.ID] = ID_list
       self.nb_BioPlate = len(BioPlateArray._STACK_ID[self.ID])
       
   def __repr__(self):
       BioPlates = [self[i] for i in range(self.nb_BioPlate)]
       return str(np.array(BioPlates))
       
   def __getitem__(self, i):
        ID = BioPlateArray._STACK_ID[self.ID][i]
        return BioPlateArray._get_bioplate_in_cache(ID)
        
   def __setitem__(self, index, value):
       self[index[0]][index[1:]] = value
        
   def change_args(func):
       def wrapper(self, *args):
            bioplate = self[args[0]]
            *args, = args[1:]
            return func(self, bioplate, *args)
       return wrapper
    
   @change_args 
   def add_value(self, bioplate, *args):
       super(type(bioplate), bioplate).add_value(*args)

      
if __name__ == "__main__":
    pl1 = BioPlate(12, 8)
    pl2 = BioPlate({"id" : 1})
    pl = pl1 + pl2
    print(pl1.ID)
    #print(pl1._BIOPLATE_CACHE)
    print(id(pl[0]) == id(pl1))
    pl.add_value(0, "B6", "value")
    pl1.add_value("G2", 'oh yheaaa')
    pl[0, 3:6, 8] = "master"
    pl1[1, 5] = "bob"
    print(pl1)
    print()
    print(pl)
