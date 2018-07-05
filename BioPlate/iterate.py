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
    """A row is symbolise by it's letter, a column by a number"""

#    @overload
#    def __new__(
#        cls,
#        plate: np.ndarray,
#        order: str = "C",
#        accumulate: bool = True,
#        OnlyValue: bool = False,
#    ) -> Iterator:  # pragma: no cover
#        pass

    def  __new__(
        cls,
        plate: np.ndarray,
        order: str = "C",
        accumulate: bool = True,
        OnlyValue: bool = False,
    ) -> Iterator:
        _ORDER: Dict[str, str] = {"C": "F", "R": "C"}
        cls.order: str = _ORDER[order]
        cls.plate: np.ndarray = plate
        cls.accumulate: bool = accumulate
        cls.OnlyValue: bool = OnlyValue
        if cls.OnlyValue:
            yield from cls._iterate()
        else:
            yield from cls.iterate()

    def __iter__(self): #pragma: no cover
        return self

    def __next__(self):#pragma: no cover
        pass

    @classmethod
    def iterate(cls) -> Iterator:
        """
        generator return [well, value]
        
        :param plate: numpy.array of plate object
        :param order: iterate by column C or by row R
        """

        if cls.accumulate:
            row, column, values = cls._acumul_iterate()
            for r, c, *v in np.nditer((row, column) + values, order=cls.order):
                yield (cls._merge_R_C_(r, c),) + tuple(map(str, v))
        else:
            for row, column, value in cls._iterate():
                for r, c, v in np.nditer((row, column, value), order=cls.order):
                    yield (cls._merge_R_C_(r, c), str(v))

    @classmethod
    def _acumul_iterate(cls) -> Tuple[str, str, Tuple[str, ...]]:
        values = []
        for row, column, value in cls._iterate():
            values.append(value)
        return row, column, tuple(values)

    @classmethod
    def _iterate(cls) -> Iterator:
        bp = cls.plate.name == "Plate"
        bpi = cls.plate.name == "Inserts"
        bps = cls.plate.name == "Stack"
        if bp:
            yield from cls.__iterate(cls.plate)
        else:
            for plat in cls.plate:
                if bps and plat.name == "Inserts":
                    for pl in plat:
                        yield from cls.__iterate(pl)
                else:
                    yield from cls.__iterate(plat)

    @classmethod
    def __iterate(
        cls, plate: np.ndarray
    ) -> Iterator:
        columns = plate[0, 1:]
        rows = plate[1:, 0:1]
        values = plate[1:, 1:]
        if cls.OnlyValue:
            yield values
        else:
            yield rows, columns, values

    @classmethod
    def _merge_R_C_(cls, row: str, column: str) -> str:
        RC = "".join(map(str, [row, column]))
        return RC
