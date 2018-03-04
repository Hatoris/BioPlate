from BioPlate.Array import BioPlateArray
from BioPlate.Manipulation import BioPlateManipulation 
from BioPlate.Stack import BioPlateStack
from BioPlate.Inserts import BioPlateInserts
from collections import OrderedDict

class BioPlate(BioPlateArray, BioPlateManipulation):
    """
    you can add on it all function of plate
    """
    def __new__(cls, *args, **kwargs):
        if len(args) == 2 or isinstance(args[0], dict):
            if kwargs.get("inserts", False):
                return BioPlateInserts(*args, **kwargs)
            else:
                return BioPlateArray.__new__(cls, *args, **kwargs)
        elif len(args) == 3:
            ID_list = []
            nb_plates, *nargs= args
            for nb_plate in range(nb_plates):
                plate = BioPlateArray.__new__(cls, *nargs, **kwargs)
                ID_list.append(id(plate))
            return BioPlateStack(ID_list)

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
              
    def save(self, plate_name, **kwargs):
        return super().save(self, plate_name, **kwargs)
        
