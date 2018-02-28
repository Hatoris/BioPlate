import numpy as np

from collections import OrderedDict
from BioPlate.Manipulation import BioPlateManipulation
from BioPlate.Array import BioPlateArray


class BioPlateStack(BioPlateManipulation):
   """
   {id_stack : [id_plate1, id_plate2]}
   """
   
   def __init__(self, ID_list):
       self.ID = id(self)
       BioPlateArray._add_stack_to_cache(self.ID, ID_list)
       
       
   def __repr__(self):
       BioPlates = [self[i] for i in range(len(self))]
       return str(np.array(BioPlates))
       
   def __getitem__(self, plate_index):
        return BioPlateArray._get_plate_in_stack( self.ID, plate_index)
        
   def __setitem__(self, index, value):
       self[index[0]][index[1:]] = value
        
   def __len__(self):
       return len(BioPlateArray._get_stack_in_cache(self.ID))
   
   def __add__(self, other):
        if type(self[0]) == type(other):
            newstack = BioPlateArray._get_stack_in_cache(self.ID)
            if other.ID not in newstack:
                newstack.append(other.ID)
            else:
                raise ValueError(f"{other} already in stack")
        elif type(self) == type(other):
            newstack = BioPlateArray._merge_stack(self.ID, other.ID) 
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)
        
   def change_args(func):
       def wrapper(self, *args):
            bioplate = self[args[0]]
            *args, = args[1:]
            return func(self, bioplate, *args)
       return wrapper
    
   @change_args 
   def add_value(self, bioplate, *args):
       super(type(bioplate), bioplate).add_value(*args)
       
   @change_args
   def add_value_row(self, bioplate, *args):
        super(type(bioplate), bioplate).add_value_row(*args)
   
   @change_args     
   def add_value_column(self, bioplate, *args):
         super(type(bioplate), bioplate).add_value_column(*args)
         
   @change_args 
   def add_values(self, bioplate, *args):
       super(type(bioplate), bioplate).add_values(*args)
         
   @change_args
   def add_multi_value(self, bioplate,*args):
       super(type(bioplate), bioplate).add_multi_value(*args)
       
   @change_args
   def evaluate(self, bioplate, *args):
        super(type(bioplate), bioplate).evaluate(*args)
        
   def iterate(self, order="C", accumulate=True):
        *BioPlates, = [self[i] for i in range(len(self))]
        yield from super()._iterate(*BioPlates, order=order, accumulate=accumulate)
