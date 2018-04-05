import numpy as np

from BioPlate.Iterate import BioPlateIterate
from collections import OrderedDict


class BioPlateCount:
    """A row is symbolise by it's letter, a column by a number"""    
      
    def __new__(cls, plate, reverse=False):
        cls.plate = plate
        cls.reverse = reverse
        cls.plate_iterated = BioPlateIterate(plate, OnlyValue=True)
        return cls.count()
   
    @classmethod     
    def __count(cls, plate):
        """

        :param plate:
        :return:
        """      
        unique, count = np.unique(plate, return_counts=True)
        count_in_dict = dict(zip(unique, count))
        count_in_dict = dict(sorted(count_in_dict.items(), key=lambda x:x[1], reverse=cls.reverse))
        return count_in_dict

    @classmethod
    def count(cls):
        if cls.plate.name == "BioPlate":
            return cls.count_BioPlate(cls.plate)
        elif cls.plate.name == "BioPlateInserts":
            return cls.count_BioPlateInserts(cls.plate)
        elif cls.plate.name == "BioPlateStack":
            return cls.count_BioPlateStack()
    
    @classmethod
    def count_BioPlateInserts(cls):
        result = {}
        result["top"] = cls.__count(next( cls.plate_iterated))
        result["bot"] =  cls.__count(next(cls.plate_iterated))
        return result

    @classmethod
    def count_BioPlate(cls):
        return cls.__count(next(cls.plate_iterated))
       
    @classmethod    
    def count_BioPlateStack(cls):
        result = {}
        n = 0
        for index, plate in enumerate(BioPlateIterate(cls.plate, OnlyValue=True)):
            if plate.name == "BioPlate":
                result[index] = cls.count_BioPlate()
                pass
            elif plate.name == "BioPlateInserts":
                try:
                    result[index] = cls.count_BioPlateInserts()
                except StopIteration:
                    break            
        return result
     