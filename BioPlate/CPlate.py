import ast
import re
import time
import numpy as np

from tabulate import tabulate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.utilitis import dimension, _LETTER
from BioPlate.plate_array import BioPlateArray, BioPlate_parameters, Slice



class BioPlateArray(np.ndarray):
    """A row is symbolise by it's letter, a column by a number"""    
    
    _BIOPLATE_CACHE = {}
    _STACK_ID = {}
    
    def __new__(cls, *args, **kwargs):
        if not isinstance(args[0], list):
            BioPlate = bioplatearray(*args, **kwargs).view(cls)
        else:
            nP = []
            for idx in args[0]:
                nP.append( CPlate._BIOPLATE_CACHE[idx])
            BioPlate = BioPlateArray(np.asarray(nP), **kwargs).view(cls)    ; 
        ID = id(BioPlate)
        if isinstance(args0], list):
            CPlate._STACK_ID[ID] = args[0]
        if ID not in CPlate._BIOPLATE_CACHE:
               CPlate._BIOPLATE_CACHE[ID] = BioPlate
        return CPlate._BIOPLATE_CACHE[ID]
         
                
      
       
class Pplate(CPlate):
    
   def __init__(self, *args, **kwargs):
       self.cplate = self
       self.ID = id(self)
      
   #def __add__(self, other):
       # ids = id(self)
       # ido = id(other)
       # return Pplate([ids, ido]) #Cp1== Cp3[0]
     
   def stack(self, other):
         ids = id(self)
         ido = id(other)
         return Pplate([ids, ido])
  
           
   def _modif_all(**kwarg):
       def __modif_all(func):
           def wrapper(self, *args, **kwargs):
               plat, col, row, val = self._args_eval(*args)
               ID = id(self)
               dim = dimension(self)
               for key, value in CPlate._STACK_ID.items():
                    if ID in value:
                        key = key
                        for i, idx in enumerate(value):
                            if ID == idx:
                                plat = i
                                break
                        PP = CPlate._BIOPLATE_CACHE[key]
                        getattr(PP, func.__name__)(plat, col, row, val)
               return func(self, *args)
           return wrapper
       return __modif_all
                

   @_modif_all()
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
     
   def __repr__(self):
      if isinstance(self.cplate, list):
          return str(np.array(self.cplate))
      return str(self.cplate)
     
   #def __getitem__(self, i):
       #ID = id(self.cplate)
       #return CPlate._BIOPLATE_CACHE[ CPlate._STACK_ID[ID].__getitem__(i)]