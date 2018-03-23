import numpy as np

from collections import OrderedDict
from BioPlate.Manipulation import BioPlateManipulation
from BioPlate.Array import BioPlateArray
from BioPlate.Stack import BioPlateStack

class BioPlateInserts(BioPlateArray, BioPlateManipulation):
    
    def __new__(cls, *args, **kwargs):
        return BioPlateArray.__new__(cls, *args, inserts=True)
        
    def __init__(self, *args, **kwargs):
        self.ID = id(self)
  
    def __add__(self, other):
        if isinstance(other, BioPlateStack):
            newstack = BioPlateArray._get_stack_in_cache(other.ID)
            newstack = [self.ID,] + newstack
        else:
            newstack = [self.ID, other.ID]
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)
  
    @property
    def top(self):
        return self[0]
   
    @property  
    def bot(self):
        return self[1]
       
    def force_position(func):
        def wrapper(self, *args, **kwargs):
            if len(self.shape) > 2:
                raise ValueError("You didn't select a part of the plate, either top or bot'")
            else:
                return func(self, *args, **kwargs)
        return wrapper
       
    @force_position
    def add_value(self, *args):
        super().add_value(*args)
        return self
        
    @force_position
    def add_value_row(self, *args):
        return super().add_value_row(*args)
        return self
   
    @force_position
    def add_value_column(self, *args):
         super().add_value_column(*args)
         return self 
         
    @force_position
    def add_values(self, *args):
       super().add_values(*args)
       return self
         
    @force_position
    def add_multi_value(self, *args):
       super().add_multi_value(*args)
       return self
       
    @force_position
    def evaluate(self, *args):
       super().evaluate(*args)
       return self
    
    def iterate(self, order="C", accumulate=True):
        yield from super()._iterate(self, order=order, accumulate=accumulate)
      
    def count(self, reverse=False):
       return super()._count(self, reverse=reverse)
       
    def save(self, plate_name, **kwargs):
        return super().save(self, plate_name, **kwargs)
        
    @force_position
    def get_value(self, *args):
       return super().get_value(*args)
       
if __name__ == "__main__":
    mul = BioPlateInserts(6, 4, inserts=True)
    mul1 = BioPlateInserts(6, 4, inserts=True)
    print(mul)
    print(mul.top.add_value("A3", "test"))
    for s in mul.iterate():
        print(s)
    print(mul.count())
    mulS = mul + mul1
    mulS.add_value(0, "top",  "C1", "plain")
    print(mulS[0].top)
    print(mulS.count())
    for st in mulS.iterate():
        print(st)
    #print(mul.bot.add_value("C5", "test2"))
    #print(mul.top.shape)
    #print(mul)