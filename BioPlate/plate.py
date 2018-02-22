from BioPlate.Array import BioPlateArray
from BioPlate.Manipulation import BioPlateManipulation 
from BioPlate.Stack import BioPlateStack
from collections import OrderedDict

class BioPlate(BioPlateArray, BioPlateManipulation):
    """
    you can add on it all function of plate
    """

    def  __init__(self, *args, **kwargs):
        self.ID = id(self)
       
    def __add__(self, other):
        if isinstance(other, BioPlateStack):
            newstack = BioPlateArray._get_stack_in_cache(other.ID)
            newstack = [self.ID,] + newstack
        else:
            newstack = [self.ID, other.ID]
        newstack = list(OrderedDict.fromkeys(newstack))
        return BioPlateStack(newstack)    
              
    def add_value(self, *args):
         super().add_value(*args)
