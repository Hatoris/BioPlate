import re
from typing import Tuple, Dict, NamedTuple, Optional, Union

import numpy as np

import BioPlate.utilitis as bpu


class Matrix(NamedTuple):  # pragma: no cover
    pos: str
    row: Union[int, slice]
    column: Union[int, slice]


class BioPlateMatrix(Matrix):
    """
    Evaluate user call and return usefull information to interact with plate. Calls are cache in dict.
    format of well :
        - B5
        - 6A
        - C[2,8]
        - 4[C,G]
        - 1-8[A,C]
        - A-G[1,8]
        - A
        - 3
    """

    _WELL_CACHE: Dict[str, bpu.EL] = dict()

    def __new__(cls, well: str) -> bpu.EL:
        well = str(well).replace(" ", "")
        BioPlateMatrix._test_for_0(well)
        if well not in BioPlateMatrix._WELL_CACHE:
            result = BioPlateMatrix._index_from_well(well)
            BioPlateMatrix._WELL_CACHE[well] = result
        return BioPlateMatrix._WELL_CACHE[well]

    @staticmethod
    def _index_from_well(well: str) -> bpu.EL:
        if BioPlateMatrix._test_row_or_column(well):
            index = BioPlateMatrix._all_row_column(well)
        else:
            column, row = BioPlateMatrix._base_row_column(well)
            index = BioPlateMatrix._index_row_column(row, column)
        return index

    @staticmethod
    def _base_row_column(well: str) -> Tuple[str, str]:
        """
        split string well to row column
        """
        row: str
        column: str
        try:  # A5, 2[B-H]
            row, column = list(reversed(sorted(filter(None, bpu._CP1.split(well)))))
        except ValueError:
            try:  # D[1-6]
                row, column = sorted(filter(None, bpu._CP2.split(well)))
            except ValueError:  # 1-5[D-F]
                row, column = bpu._CP3.findall(well)
        return column, row

    @staticmethod
    def _multi_row_column(multi: str) -> Tuple[str, str]:
        """
        From multi value return only row or column
        """
        comp = re.compile("(\w+)")
        multi1, multi2 = list(sorted(filter(comp.search, re.split("(\W)", multi))))
        return multi1, multi2

    @staticmethod
    def _index_row_column(row: str, column: str) -> bpu.EL:
        """
        get split of row or  column in multi value
        """
        comp = re.compile("(\w+)")
        lrow = len(row)
        lcolumn = len(re.findall(comp, column))
        if lrow > 1 and lcolumn > 1:
            value = BioPlateMatrix.__m_row_m_column(row, column)
            return value
        elif lrow == 1 and lcolumn == 1:
            ro = BioPlateMatrix._well_letter_index(row)
            return bpu.EL("W", int(ro), int(column))
        elif lrow > 1 and lcolumn == 1:
            row1, row2 = list(
                map(
                    BioPlateMatrix._well_letter_index,
                    BioPlateMatrix._multi_row_column(row),
                )
            )
            return bpu.EL("C", slice(int(row1), int(row2) + 1, 1), int(column))
        else:  # lcolumn > 1 and lrow == 1:
            column1, column2 = sorted(
                map(int, BioPlateMatrix._multi_row_column(column))
            )
            ro = BioPlateMatrix._well_letter_index(row)
            return bpu.EL("R", int(ro), slice(column1, column2 + 1, 1))

    @staticmethod
    def __m_row_m_column(row: str, column: str) -> bpu.EL:
        val = re.compile("(\w+)")
        comp = lambda x: list(BioPlateMatrix._multi_row_column(x))
        iterator, selector = list(map(comp, [row, column]))
        try:
            row1, row2 = list(map(BioPlateMatrix._well_letter_index, selector))
            column1, column2 = sorted(map(int, iterator))
            return bpu.EL(
                "C",
                slice(int(row1), int(row2) + 1, 1),
                slice(int(column1), int(column2) + 1, 1),
            )
        except ValueError:
            row1, row2 = list(map(BioPlateMatrix._well_letter_index, iterator))
            column1, column2 = sorted(map(int, [selector[0], selector[1]]))
            return bpu.EL(
                "R", slice(int(row1), int(row2) + 1, 1), slice(column1, column2 + 1, 1)
            )

    @staticmethod
    def _well_letter_index(row_letter: str) -> int:
        """
        get index for a given letter (eg : C)
        
        :param row_letter: C => letter of a row
        :return: 3 => index of row C in plate.array
        """
        return np.searchsorted(bpu._LETTER, row_letter) + 1

    @staticmethod
    def _test_for_0(well: str) -> Optional[str]:
        zero = re.compile("(^\D*0\D*$)")
        test = list(filter(zero.search, re.split("(\d+)", well)))
        if not test:
            return None
        else:
            raise ValueError(f"well = {well} is not allowed, column 0 is forbiden")

    @staticmethod
    def _all_row_column(well: str) -> bpu.EL:
        try:
            index = int(well)
            return bpu.EL("C", slice(1, None), index)
        except ValueError:
            index = BioPlateMatrix._well_letter_index(well)
            return bpu.EL("R", index, slice(1, None))

    @staticmethod
    def _test_row_or_column(well: str) -> bool:
        if isinstance(well, int):  # int return true
            return True
        elif isinstance(well, str):  # str to int return true
            try:
                int(well)
                return True
            except ValueError:  # here it's string that can't be convert
                if len(well) == 1:
                    return True
                else:
                    return False
