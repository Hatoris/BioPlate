from typing import (
    Dict,
    List,
    Tuple,
    Optional,
    Union,
    Any,
    overload,
    Sequence,
    Generator,
    Iterator,
)

import numpy as np

class BioPlateIterate:

    def __init__(self, plate, order="C", accumulate=True, OnlyValue=False):
        _ORDER: Dict[str, str] = {"C": "F", "R": "C"}
        self.order: str = _ORDER[order]
        self.plate: np.ndarray = plate
        self.accumulate: bool = accumulate
        self.OnlyValue: bool = OnlyValue

    def __iter__(self):
        columns = self.plate[0, 1:]
        rows = self.plate[1:, 0:1]
        values = self.plate[1:, 1:]
        # if self.OnlyValue:
        #     for value in np.nditer(values, order=self.order):
        #         yield tuple(str(value))
        # else:
        for row, column, value in np.nditer((rows, columns, values), order=self.order):
            yield self._merge_R_C_(row, column), str(value)

    def __next__(self):
        if self.OnlyValue:
            for value in iter(self):
                return tuple(str(value))
        else:
            for row, column, value in  iter(self):
                return (self._merge_R_C_(row, column), str(value))
        
    def _merge_R_C_(self, row: str, column: str) -> str:
        RC = "".join(map(str, [row, column]))
        return RC
    
