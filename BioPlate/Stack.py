import numpy as np
from BioPlate.Manipulation import BioPlateManipulation
from BioPlate.Array import BioPlateArray
#from BioPlate.Plate import BioPlate

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
        
   def __add__(self, other):
        if type(self[0]) == type(other):
            newstack = BioPlateArray._STACK_ID[self.ID]
            newstack.append(other.ID)
        elif type(self) == type(other):
            newstack = BioPlateArray._STACK_ID[self.ID] + BioPlateArray._STACK_ID[other.ID]
        #newstack = list(set(newstack))
        #print(newstack)
        return BioPlateStack(newstack)
        
   def change_args(func):
       def wrapper(self, *args):
            bioplate = self[args[0]]
            *args, = args[1:]
            return func(self, bioplate, *args)
       return wrapper
    
   @change_args 
   def add_value(self, bioplate, *args):
       print(type(bioplate))
       print(type(bioplate) == bioplate.__class__)
       super(type(bioplate), bioplate).add_value(*args)