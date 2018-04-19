import numpy as np
import pyexcel_xlsx as pex
import pyexcel as pe
import sys

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data
from functools import lru_cache
from BioPlate.Plate import BioPlate
from collections import OrderedDict


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
   def __init__(self, file_name, sheets=None, header = True, Inserts = False, plate_infos=None, stack = True):
       """
       header : plate represented in excel have header
       sheets : list of sheet name to select from excel file if None all sheet will be transform
       plate_infos : dict : {"sheet_name" : NAME,  "row" : 9, "column" : 12}
       if header is false, plate_infos should be provide. If sheets is None all sheets will be processes, 
       
       give excel book name, if no sheets list( shoukd be always in list) do on all sheets, return dict of sheet_name : list of bioplate
       """
       self.file_name = file_name
       self.sheets = sheets
       self.header = header
       self.plate_infos = plate_infos
       self.Inserts = Inserts
       self.stack = stack
       try:
           self.loaded_file = pex.get_data(self.file_name)
       except FileNotFoundError:
           print(f"{self.file_name} not found !")
           sys.exit(1)
       self.working = {}
       self._sheets_choices
       #print("WORKING ", self.working)
       self.working_numpy = {}
       self._get_npArray
       #print("WORKING NUMPY", self.working_numpy)
       self.working_clean_npArray = {} #add value to get great plate representation
       self._clean_npArray
       #print("WORKING clean", self.working_clean_npArray)
       self.BioPlate_representation = {}
       self._get_BioPlate
      
    
   @property
   def _sheets_choices(self):
        """
        return a dict with apropriate infos
        
        """
        if self.sheets is not None:
            for sheet_name in self.sheets:
                self.working[sheet_name] = self._remove_empty_sheet( self.loaded_file)[sheet_name]
        else:
             self.working = self._remove_empty_sheet(self.loaded_file)
        
   @property               
   def  _get_npArray(self):
         """
         split array if necessary 
         """         
         for sheet_name, value in self.working.items():
             self.working_numpy[sheet_name] = self.__split_representation(np.array(value))
      
   @property
   def _clean_npArray(self):
        """
        add miasing value to each numpy array
        """
        for sheet_name, value in self.working_numpy.items():
            self.working_clean_npArray[sheet_name] = []
            for npArray in value:
                self.working_clean_npArray[sheet_name].append(self.numpy_reshape(npArray))
    
   @property               
   def _get_BioPlate(self):
       for sheet_name, value in self.working_clean_npArray.items():
           self.BioPlate_representation[sheet_name] = []
           if self.Inserts:
               nIterValue = iter(value)
               for npTopArray in nIterValue:
                   self.BioPlate_representation[ sheet_name].append( self._get_Inserts_representation(npTopArray, next(nIterValue)))
           else:
               for npArray in value:
                   self.BioPlate_representation[ sheet_name].append( self._get_BioPlate_representation(npArray))
               self._get_BioPlate_representation(npArray)

   def _remove_empty_sheet(self, dict_to_clean):
        clean_dict = OrderedDict([(key, value) for key, value in dict_to_clean.items() if value])
        return clean_dict
      
   @property
   @lru_cache(maxsize=None)
   def to_numpy(self):
      new_values = {}
      for sheet_name, values in self.loaded_file.items():
          if values:
              if self.sheets and sheet_name in self.sheets:
                  new_values[sheet_name] = np.array(values)
              elif self.sheets is None:
                  new_values[sheet_name] = np.array(values)        
      return new_values     

   def numpy_reshape(self, npArray):
        """
        fill blanck to get a great repreaentation
        """
        column, row = self._column_row(npArray)
        ln = np.vectorize(len)
        liln = lambda plate : list(map(len, plate))
        val = ln(npArray)
        n_row = len(val)
        if n_row < row: #add row (empty list)
            npArray = self._add_row(npArray, row - n_row)
        npArray = self._add_column(npArray, column)
        nval = ln(npArray)
        return npArray
 
   def _add_row(self, npArray,  nb_row_to_add):
        liArray = list(npArray)
        for i in range(nb_row_to_add):
            liArray.append([])
        npArray = np.array(liArray)
        return npArray

   def _add_column(self, npArray,  nb_total_column, default="" ):
         liArray = list(npArray)
         ln = lambda plate : list(map(len, plate))
         for row in liArray:
             n_column = len(row)
             missing = nb_total_column - n_column
             for _ in range(missing):
                 row.append(default)
         npArray = np.array(liArray)
         return npArray                                                                       
                            
   @property
   @lru_cache(maxsize=None)
   def loaded_sheets(self):
        return [sheet_name for sheet_name in self.loaded_file]
       
   def _get_plate_representation_value(self, npArray):
        if not self.header:
            return npArray
        else:
            try:
                return npArray[1:,1:]
            except IndexError:
                return None           
          
   def _get_BioPlate_representation(self, npArray):
        valueArray = self._get_plate_representation_value(npArray)
        column, row = self._column_row(valueArray)
        plate = BioPlate(column, row)
        plate[1:,1:] = valueArray.astype("U100")
        return plate
        
   def _get_Inserts_representation(self, npTopArray, npBotArray):
        valueTopArray = self._get_plate_representation_value(npTopArray)
        valueBotArray = self._get_plate_representation_value(npBotArray)
        column, row = self._column_row(valueTopArray)
        plate = BioPlate(column, row, inserts=True)
        plate[0, 1:,1:] = valueTopArray.astype("U100")
        plate[1, 1:,1:] = valueBotArray.astype("U100")
        return plate
   
   def __split_representation(self, multiArray):
       #rm = lambda x : True if getattr(x, "size") > 0 and x[0] != list([]) else False
       rm = lambda x : True if getattr(x, "size") > 1 else False
       if self.header:
           isempty = np.vectorize(any)
           mask = isempty(multiArray)
           index = np.argwhere(mask == False).flatten()
           index = list(ialone for tupi in map(lambda i: (i, i+1), index) for ialone in tupi)
           results = np.array_split(multiArray, index)
           results = list(filter(rm, results))
       else:
           row = self.plate_infos.get("row")
           len_mu = len(multiArray)
           index = [(x, x+1) for x in range(row, len_mu, row)]
           index = list(ialone for tupi in index for ialone in tupi)
           results = np.array_split(multiArray, index)
           results = list(filter(rm, results))
       return results 
       
   def _column_row(self, plate):
       """
       this function is to find row column
       
       """
       if self.header:
           column = len(plate[0])
           row = len(plate)
       else:
           column = self.plate_infos.get("column")
           row = self.plate_infos.get("row")
       return column, row
        
        
        
