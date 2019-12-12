"""This module implemented all functionality to set value on a BioPlate object. 

To assigne a value on a plate, we need the coordinate represented by column and row value. 
Several values can be assigned in a loop.  
"""

from typing import List,Generator,Dict, Union,Tuple, Yields

from BioPlate.core.matrix import well_to_index
import numpy.core.defchararray as ncd



class Set:


    def __init__(self, *elements, merge=False):
        self.bioplate = bioplate
        self.set_iterator = iterate_elements(*elements)
        self.merge = merge

class OneSet:

    def __init__(self, well, index, value, merge=False):
        self.well = well
        self.index = index 
        self.part = len(value) if isinstance(value, (list, tuple)) else None
        self.merge = merge
        self.value = value


    def _basic_set(self, bioplate):
        """
        Evaluate if value should be apply to __setitem__ or slice of it
        
        """
        if merge:
            value = self.merge_value(bioplate)
        if part:
            self._set_part(index, value, part)
        else:
            self._set(index, value)

    def merge_value(self, bioplate):
        """
        Update value with existing value of selected well and merge it
        """
        previous_value = bioplate[self.index.row, self.index.column][:self.part]
        return ncd.add(previous_value, self.value)
                        
    def set(self, index, value):
        """
        Call __setitem__ of bioplate and qssign value on it
        """
        self.__setitem__((index.row, index.column), value)

    def set_part(self, index, value, part):
        """
        Call __setitem__ and slice it to fit the number of value to assign
        """
        #self[index.row, index.column][:part] = value
        try:
            self.__getitem__((index.row, index.column)).__setitem__( slice(None, part, None), value)
        except AttributeError:
            raise ValueError("Cannot assign index to plate")

    def set_list(self,bioplate):
        """
        Evaluate if a list should be reshape  or setitem should be sliced
        """
        plate_shape = bioplate[self.index.row, self.index.column].shape
        len_plate_shape = len(plate_shape)
        if len_plate_shape > 1:
            self._set_reshape(plate_shape)
        else:
            self._basic_set(index, value, merge, part)
            
    def set_reshape(self, plate_shape):
        """
        Reshape value if needed
        """
        if index.pos == "R":
            try:
                value = np.reshape(self.value, (plate_shape[0], 1))
            except ValueError:
                raise ValueError(f"cannot reshape {self.value} ({self.part}) based on well : {self.well} ")
        self._basic_set(self.value)           
        


def iterate_elements(*elements) -> Yields:
    """Create a generator from well if its an iterable
    
    Parameters
    ----------
    well : Union[List, Tuple, Dict]
        An iterable containg pairs of coordinate and value
    
    Yields
    -------
    Generator
        yield a tuple of well and value to assigned
    """
    well, value = elements if len(elements) == 2 else elements, None 

    if value is not None:
        yield well, well_to_index(well), value
    else:
        generator = well.items() if isinstance(well, dict) else well
        for well, value in generator:
            yield well, well_to_index(well), value






