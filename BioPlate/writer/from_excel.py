import pyexcel_xlsx as pex
import sys
from typing import List, Tuple, Dict, Callable, Union, Iterable, Any, Iterator, overload

import pyexcel_xlsx as pex

from BioPlate import BioPlate
from BioPlate.inserts import Inserts
from BioPlate.plate import Plate
from BioPlate.stack import Stack
from BioPlate.utilitis import _LETTER


class BioPlateFromExcel:
    """ This class should be instanciate with those parameters :func:`~BioPlate.writer.from_excel._BioPlateFromExcel.__init__`
    
       Returns
       ------------
       bioplate_dict : dict
           Dict with sheetname as key and list of bioplate object as value
    """
    def __new__(cls, *args, **kwargs):
        BPFE = _BioPlateFromExcel(*args, **kwargs)
        return BPFE._get_BioPlate_object()


class _BioPlateFromExcel:

    def __init__(self, file_name : str, sheets : List[str] =None, plate_infos : Dict[str, Dict]=None):
        """This class load plate representation and data fron excel file. If no sheetnames are specifed all sheets will be process. If plate are only data and no headers are present, you should provide a plate information. Eg : {"sheetname" : { "row" : 9, "column" : 12, "stack" : True, "type" : "BioPlate"}}
        
        Parameters
        --------------------
       sheets : list, default None 
           List of sheet name to process if None all sheet will be process
       plate_infos : dict, default None
           Should be provide if no header are present in given sheet. Eg : {"sheetname" : { "row" : 9, "column" : 12, "stack" : True, "type" : "BioPlate"}}           
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
        """Get only sheet with element in it and discard empty ones.
        
        Returns
        ------------
        Dict_of_sheet : dict
            keys are sheet name, values are list of element
            
        """
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
        """Guess or extract plate informations from a list of data
        
        Parameters
        ----------
        value : List[List]
            list of element return by `pyexcel_xlsx.get_data`_
        sheetname : str
            Name of sheet to process
             
            .. _pyexcel_xlsx.get_data: https://pythonhosted.org/pyexcel-xlsx/index.html?highlight=get#read-from-an-xlsx-file
            
        Returns
        --------
        Type : Plate or Inserts
            Basic object type (Plate or Inserts)
        stack : Boolean, dafault False
            values are a stack of basic object type (Plate or Inserts)
        column : int
             number of column in plate
        row : int
             number of row in plate
              
         Exemples
         -----------------         
        >>> from BioPlate.from_excel import _BioPlateFromExcel
        >>> BPFE = _BioPlateFromExcel("path/to/my_file.xlsx", sheetname = ["sheet1"])
        >>> BPFE.loaded_file["sheet1"]
        [[, 1, 2, 3], ["A", "t1", "t2", "t3"], ["B", "y1", "y2", "y3"]]
        >>> BPFE._get_plate_informations(BPFE.loaded_file["sheet1"], "sheet1")
        (Plate, False, 3, 2)
        
        """
        if self.plate_infos is None:
            # do stuff with header
            Type = self._guess_type(value)
            stack = self._get_stack(value)
            column, row = self._guess_column_row(value)
        else:
            # do stuff with plate infos
            TYPE = {"Plate": Plate, "Inserts": Inserts}
            infos = self.plate_infos[sheetname]
            header = infos.get("header", False)
            stack = infos.get("stack", False)
            Type = TYPE.get(infos.get("type", "Plate"))
            column = infos.get("column")
            row = infos.get("row")
        return Type, stack, column, row

    def is_insert(self, value: List[List]) -> bool:
        val = value[0][0]
        if val in ["TOP", "BOT"]:
            return True
        return False

    @overload
    def _guess_type(self, value : List[List]) -> Plate:#pragma: no cover
        pass

    @overload
    def _guess_type(self, value : List[List]) -> Inserts:#pragma: no cover
        pass

    def _guess_type(self, value):
        """this function have to guess from list[list] the shape of plate and return plate class to use"""
        if self.is_insert(value):
            return Inserts
        else:
            return Plate

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
                    return True  # two Plate
            else:
                return False  # a Plate alone
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

    def _get_BioPlate_object(self) -> Dict[str, Union[Plate, Inserts, Stack]]:
        final = dict()
        for sheetname, value in self.no_empty_sheets.items():
            if self._get_stack(value, sheetname):
                final[sheetname] = Stack(
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
    def _instance_of_plate(self, Type : Callable[[int, int], Plate], column : int, row : int):#pragma: no cover
        pass

    @overload
    def _instance_of_plate(self, Type : Callable[[int, int], Inserts], column : int, row : int):#pragma: no cover
        pass

    def _instance_of_plate(self, Type , column , row):
        return Type(column, row)

    def _get_one_plate(self, values: List[List], sheetname: str) -> Iterator:
        Type, stack, column, row = self._get_plate_informations(values, sheetname)
        plate = self._instance_of_plate(Type, column, row)
        if plate.name == "Plate":
            plates, rest = self._pre_bp_iterate(values, row)
            for i, val in self._iterate_bp_value(plates, row):
                plate.set(_LETTER[i], val)
        elif plate.name == "Inserts":
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
