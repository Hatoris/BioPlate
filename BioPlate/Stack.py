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
       if isinstance(ID_list[0], int):
           BioPlateArray._add_stack_to_cache(self.ID, ID_list)
       else:
           new_ID_list = []
           for BP in ID_list:
               ID = id(BP)
               new_ID_list.append(ID)
               BioPlateArray._add_plate_in_cache(ID, BP)
           BioPlateArray._add_stack_to_cache(self.ID, new_ID_list)
             
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
            if len(bioplate.shape) == 2:
                *args, = args[1:]
                return func(self, bioplate, *args)
            else:
                position, *args = args[1:]
                #t =  {"top" : 0, "bot" : 1}
                bioplate = getattr(bioplate, position)
                return func(self, bioplate, *args)
       return wrapper
    
   def pass_all_plate(func):
        def wrapper(self, *args, **kwargs):
            *BioPlates, = [self[i] for i in range(len(self))]
            return func(self, *BioPlates, **kwargs)
        return wrapper
        
   @change_args 
   def add_value(self, bioplate, *args):
       bioplate.add_value(*args)
       return self
       
   @change_args
   def add_value_row(self, bioplate, *args):
        bioplate.add_value_row(*args)
        return self
   
   @change_args     
   def add_value_column(self, bioplate, *args):
         bioplate.add_value_column(*args)
         return self 
         
   @change_args 
   def add_values(self, bioplate, *args):
       bioplate.add_values(*args)
       return self
         
   @change_args
   def add_multi_value(self, bioplate,*args):
       bioplate.add_multi_value(*args)
       return self
       
   @change_args
   def evaluate(self, bioplate, *args):
       bioplate.evaluate(*args)
       return self
    
   @pass_all_plate    
   def iterate(self, *BioPlates, order="C", accumulate=False):
        yield from super()._iterate(*BioPlates, order=order, accumulate=accumulate)
      
   @pass_all_plate
   def count(self, *BioPlates, reverse=False):
       return super()._count(*BioPlates, reverse=reverse)

   def save(self, plate_name, **kwargs):
        BioPlates = [self[i] for i in range(len(self))]
        return super().save(BioPlates, plate_name, **kwargs)
       
   @change_args
   def get_value(self, bioplate, *args):
       return bioplate.get_value(*args)
       #return self