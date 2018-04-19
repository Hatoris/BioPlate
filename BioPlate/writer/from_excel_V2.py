import numpy as np
import pyexcel_xlsx as pex
import pyexcel as pe
import sys

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data
from functools import lru_cache
from BioPlate.Plate import BioPlate
from BioPlate.Inserts import BioPlateInserts
from BioPlate.Stack import BioPlateStack
from BioPlate.utilitis import _LETTER
from collections import OrderedDict
from typing import List, Tuple, Dict, Any, Callable

class BioPlateFromExcel:
   """
   thia class is for load plate representation and data fron excel file
   one sheet => one plate
   one sheet => multi plate
   multi sheet => one plate per sheet
   1. Open excel file
   2. Sheets are specifed ? If no, use all sheets
   3. Header are present ? If no, provide plate_infotmation
   
   """
   def __init__(self, file_name, sheets= None, plate_infos= None):
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
           print(f"{self.file_name} not found !")
           sys.exit(1)
       self.no_empty_sheets = self._get_no_empty_sheets()
                      
   def _get_no_empty_sheets(self) -> Dict[str, List]:
       """return a dict without empty sheet"""
       no_empty_sheet = dict()
       for sheetname, value in self.loaded_file.items():
            if not value:
                continue
            no_empty_sheet[sheetname] = value   
       return no_empty_sheet

   def _get_plate_informations(self, value) -> Tuple[Callable, bool, int, int]:
       """type, plate object in stack with column snd row"""
       if self.plate_infos is None:
               #do stuff with header
               type, stack = self._guess_type(value)
               column, row = self._guess_column_row(value)               
       else:
               #do stuff with plate infos
               infos = plate_infos[sheetname]
               header = infos.get("header",  False)
               stack = infos.get("stack", False)
               type = infos.get("type", BioPlate)
               column = infos.get("column")
               row = infos.get("row")
       return type, stack, column, row
           
   def _guess_type(self, value:List[List]) -> Tuple[Callable, bool]:
       """this function have to guess from list[list] the shape of plate and return plate class to use and if is a stack or note """
       blank_line = value.count([])
       if blank_line >= 1:
            if  blank_line > 1:
                stack = True
            else:
                 stack = False
            if value[0][0] in ["TOP", "BOT"]:
                return BioPlateInserts, stack
            else:
                 return BioPlate, True
       else:
           return BioPlate, False
         
   def _guess_column_row(self, value:List[List]) -> Tuple[int, int]:
       """get column and row number from representation with header, -1 is to remove header"""
       column = len(value[0]) - 1
       try:
           row = value.index(list()) - 1
       except ValueError:
           row = len(value) - 1
       return column, row

   def _get_BioPlate_object(self):
        final = dict()
        for sheetname, value in self.no_empty_sheets.items():
           final[sheetname] = next(self._get_one_plate1(value))
        return final

   def _get_value_for_plate(self, value):
       type, stack, column, row = self._get_plate_informations(value)
       plate = self._instance_of_plate(type, column, row)
       forStack = []
       return BioPlateStack(forStack)
    
   def _get_one_plate(self, value):
       type, stack, column, row = self._get_plate_informations(value)
       plate = self._instance_of_plate(type, column, row)
       if plate.name == "BioPlate":
           for i, val in self._iterate_bp_value(value, row):
                plate.set(_LETTER[i], val)
       elif plate.name == "BioPlateInserts":
           for i, position, val in self._iterate_bpi_value(value, row):
               getattr(plate, position).set(_LETTER[i], val)
       else:
              return None
       return plate 
      
   def _iterate_bp_value(self, value:List[List], row:int) -> Tuple[int, List]:
       plate, rest = self._pre_bp_iterate(value, row)
       if self.plate_infos is None:
           for i, val in enumerate(plate[1:]):
               i = i % row
               yield i, val[1:]
       else:
           for i, val in enumerate(plate):
               i = i % row
               yield i, val        
       if rest:
           yield from self._iterate_bp_value(rest, row)

   def _pre_bp_iterate(self, value, row):
        if self.plate_infos is None:
            yield value[:row+1], value[row+2:]
        else:
            yield value[:row], value[row+1:]
    
            
   def _iterate_bpi_value(self, value:List[List], row:int) -> Tuple[int, List]:
       plates, rest = self._pre_bpi_iterate(value, row)
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
       if rest:
           yield from self._iterate_bpi_value(rest, row)                 
                                    
   def _pre_bpi_iterate(self, value, row):
        if self.plate_infos is None:
            #2 plate + 2 header + 1 empty
            rowS = row + row + 2 + 1 
            return [value[:row + 1], value[row + 2:rowS]], value[rowS:]
        else:
            #2 plate + 1 empty, no header
            rowS = row + row + 1
            return [value[:row], value[row+1:rowS]], value[rowS:]                
                                                                                      
   def _instance_of_plate(self, type, column, row):
        return type(column, row)                 

   def  _get_one_plate1(self, values):
       type, stack, column, row = self._get_plate_informations(values)
       plate = self._instance_of_plate(type, column, row)
       if plate.name == "BioPlate":
            plates, rest = self._pre_bp_iterate(values, row)
            print(plates)
            for i, val in self._iterate_bp_value1(plates, row):
                print(i, val)
                plate.set(_LETTER[i], val)
       elif plate.name == "BioPlateInserts":
            plates, *rest = self._pre_bpi_iterate(values, row)
            for i, position, val in self._iterate_bpi_value1(plates, row):
               getattr(plate, position).set(_LETTER[i], val)
       yield plate
       if rest:
           yield from self._get_one_plate(rest)
        
   def _iterate_bpi_value1(self, plates:List[List], row:int) -> Tuple[int, List]:
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
          
   def _iterate_bp_value1(self, plate:List[List], row:int) -> Tuple[int, List]:
       if self.plate_infos is None:
           for i, val in enumerate(plate[1:]):
               i = i % row
               yield i, val[1:]
       else:
           for i, val in enumerate(plate):
               i = i % row
               yield i, val