"""This module implemented all functionality to set value on a BioPlate object. 

To assigne a value on a plate, we need the coordinate represented by column and row value. 
Several values can be assigned in a loop.  
"""

from typing import List,Generator,Dict, Union,Tuple, Yields

from BioPlate.core.matrix import well_to_index




class Set:


    def __init__(self, *elements, merge=False):
        self.bioplate = bioplate
        self.set_iterator = iterate_elements(*elements)
        self.merge = merge

class OneSet:

    def __init__(self, well, value, merge=False):
        self.well = well 
        self.value = value 
        self.part = len(value) if isinstance(value, (list, tuple)) else 1
        self.merge = merge 


    def merged_value(self, bioplate)


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
    well_human, value = elements if len(elements) == 2 else elements, None 

    if value is not None:
        yield well_to_index(well_human), value
    else:
        generator = well_human.items() if isinstance(well_human, dict) else well_human
        for well_human, value in generator:
            yield well_to_index(well_human), value






