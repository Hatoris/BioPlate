from BioPlate.Array import BioPlateArray
from BioPlate.Manipulation import BioPlateManipulation
from BioPlate.Stack import BioPlateStack
from BioPlate.utilitis import dimension

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
