import pyexcel_xlsx as pex
import sys
from typing import List, Tuple, Dict, Callable, Union, Iterable, Any, Iterator, overload

import pyexcel_xlsx as pex

from BioPlate import BioPlate
from BioPlate.inserts import BioPlateInserts
from BioPlate.plate import BioPlatePlate
from BioPlate.stack import BioPlateStack
from BioPlate.utilitis import _LETTER


class BioPlateFromExcel:
    def __new__(cls, *args, **kwargs):
        BPFE = _BioPlateFromExcel(*args, **kwargs)
        return BPFE._get_BioPlate_object()


class _BioPlateFromExcel:
    """
   thia class is for load plate representation and data fron excel file
   one sheet => one plate
   one sheet => multi plate
   multi sheet => one plate per sheet
   1. Open excel file
   2. Sheets are specifed ? If no, use all sheets
   3. Header are present ? If no, provide plate_infotmation
   
   """

    def __init__(self, file_name, sheets=None, plate_infos=None):
        """
       header : plate represented in excel have header
       sheets : list of sheet name to select from excel file if None all sheet will be transform
       plate_infos : dict : {"sheetname" : { "row" : 9, "column" : 12, "stack" : True, "type" : "BioPlate"}}
       if header is false, plate_infos should be provide. If sheets is None all sheets will be processes, 
       
       give excel book name, if no sheets list( shoukd be always in list) do on all sheets, return dict of sheet_name : list of bioplate
       """
        self.file_name = file_name
        self.sheets = sheets
        self.plate_infos = plate_infos
        try:
            self.loaded_file = pex.get_data(self.file_name)
        except FileNotFoundError:
            sys.exit(f"{self.file_name} not found !")
        self.no_empty_sheets = self._get_no_empty_sheets()

    def _get_no_empty_sheets(self) -> Dict[str, List]:
        """return a dict without empty sheet"""
        no_empty_sheet = dict()
        for sheetname, value in self.loaded_file.items():
            if value:
                if self.sheets:
                    if sheetname in self.sheets:
                        no_empty_sheet[sheetname] = value
                else:
                    no_empty_sheet[sheetname] = value
        return no_empty_sheet

    def _get_plate_informations(
        self, value: List[List], sheetname: str
    ) -> Tuple[Callable, bool, int, int]:
        """type, plate object in stack with column snd row"""
        if self.plate_infos is None:
            # do stuff with header
            Type = self._guess_type(value)
            stack = self._get_stack(value)
            column, row = self._guess_column_row(value)
        else:
            # do stuff with plate infos
            TYPE = {"BioPlatePlate": BioPlatePlate, "BioPlateInserts": BioPlateInserts}
            infos = self.plate_infos[sheetname]
            header = infos.get("header", False)
            stack = infos.get("stack", False)
            Type = TYPE.get(infos.get("type", "BioPlatePlate"))
            column = infos.get("column")
            row = infos.get("row")
        return Type, stack, column, row

    def is_insert(self, value: List[List]) -> bool:
        val = value[0][0]
        if val in ["TOP", "BOT"]:
            return True
        return False

    @overload
    def _guess_type(self, value : List[List]) -> BioPlatePlate:#pragma: no cover
        pass

    @overload
    def _guess_type(self, value : List[List]) -> BioPlateInserts:#pragma: no cover
        pass

    def _guess_type(self, value):
        """this function have to guess from list[list] the shape of plate and return plate class to use"""
        if self.is_insert(value):
            return BioPlateInserts
        else:
            return BioPlatePlate

    def _get_stack(self, value: List[List], sheetname: str = None) -> bool:
        """this function have to guess from list[list] if it is a stack or not """
        if self.plate_infos is None:
            blank_line = value.count([])
            if blank_line >= 1:
                if blank_line > 1:
                    stack = True
                else:
                    stack = False
                if self.is_insert(value):
                    return stack
                else:
                    return True  # two BioPlatePlate
            else:
                return False  # a BioPlatePlate alone
        else:
            return self.plate_infos[sheetname].get("stack", False)

    def _guess_column_row(self, value: List[List]) -> Tuple[int, int]:
        """get column and row number from representation with header, -1 is to remove header"""
        column = len(value[0]) - 1
        try:
            row = value.index(list()) - 1
        except ValueError:
            row = len(value) - 1
        return column, row

    def _get_BioPlate_object(self) -> Dict[str, Union[BioPlatePlate, BioPlateInserts, BioPlateStack]]:
        final = dict()
        for sheetname, value in self.no_empty_sheets.items():
            if self._get_stack(value, sheetname):
                final[sheetname] = BioPlateStack(
                    list(self._get_one_plate(value, sheetname))
                )
            else:
                final[sheetname] = next(self._get_one_plate(value, sheetname))
        return final

    def _pre_bp_iterate(self, value : List[List], row : int)-> Iterator:
        if self.plate_infos is None:
            # 1 header + 1 empty
            yield value[: row + 1]
            yield value[row + 2 :]
        else:
            # 1 header + 1 empty
            yield value[:row]
            yield value[row + 1 :]

    def _pre_bpi_iterate(self, value : List[List], row : int)-> Iterator:
        if self.plate_infos is None:
            # 2 plate + 2 header + 2 empty
            rowS = row + row + 2 + 2
            yield [value[: row + 1], value[row + 2 : rowS]]
            yield value[rowS:]
        else:
            # 2 plate + 2 empty, no header
            rowS = row + row + 2
            yield [value[:row], value[row + 1 : rowS]]
            yield value[rowS:]

    @overload
    def _instance_of_plate(self, Type : Callable[[int, int], BioPlatePlate], column : int, row : int):#pragma: no cover
        pass

    @overload
    def _instance_of_plate(self, Type : Callable[[int, int], BioPlateInserts], column : int, row : int):#pragma: no cover
        pass

    def _instance_of_plate(self, Type , column , row):
        return Type(column, row)

    def _get_one_plate(self, values: List[List], sheetname: str) -> Iterator:
        Type, stack, column, row = self._get_plate_informations(values, sheetname)
        plate = self._instance_of_plate(Type, column, row)
        if plate.name == "BioPlatePlate":
            plates, rest = self._pre_bp_iterate(values, row)
            for i, val in self._iterate_bp_value(plates, row):
                plate.set(_LETTER[i], val)
        elif plate.name == "BioPlateInserts":
            plates, rest = self._pre_bpi_iterate(values, row)
            for i, position, val in self._iterate_bpi_value(plates, row):
                getattr(plate, position).set(_LETTER[i], val)
        yield plate
        if rest:
            yield from self._get_one_plate(rest, sheetname)

    def _iterate_bpi_value(
        self, plates: List[List], row: int
    ) -> Union[Iterator[Tuple[int, str, List]]]:
        position = "top"
        for plate in plates:
            if self.plate_infos is None:
                for i, val in enumerate(plate[1:]):
                    i = i % row
                    yield i, position, val[1:]
            else:
                for i, val in enumerate(plate):
                    i = i % row
                    yield i, position, val
            position = "top" if position == "bot" else "bot"

    def _iterate_bp_value(self, plate: List[List], row: int) -> Iterator[Tuple[int, List]]:
        if self.plate_infos is None:
            for i, val in enumerate(plate[1:]):
                i = i % row
                yield i, val[1:]
        else:
            for i, val in enumerate(plate):
                i = i % row
                yield i, val
