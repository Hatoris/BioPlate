import ast
import re
import time
import operator
import inspect
import numpy as np
import BioPlate.utilitis as bpu

from tabulate import tabulate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.Matrix import BioPlateMatrix


"""
add value : add value to one wells (eg : 'B5)
add_value_row : add the same values on multiple row (eg: 'C[3,12]', 'test')
add_value_column : add the same values on multiple column (eg: '3[A,H]', 'test4')
 '1-3[B,E]' == '1[B,E]', '2[B,E]', '3[B,E]' == 'B1', 'C1', 'D1', 'E1', 'B2', 'C2' ... == '1B', '1C' ... 
    ---------     ----------------------------    --------------------------------------------------------
    condensed             medium                                       small                              : form assignation

self._eval_well_value is slower than directly call BioPlateMatrix and assign properly to each part of plate. Avoid self._eval except if you can't know in advance return positiln of BioPlateMatrix'.

eg: self._eval_well_value("A[2-8]", "test") is slower than row, col1, col2 = BioPlateMatrix("A[2-8]"), Plate[row, col1:col2] = value



"""


class BioPlateManipulation:
    """A row is symbolise by it's letter, a column by a number"""    
                
    def _args_analyse(self, *args):
        #add_value, add_row_value, add_column_value
        dict_in = any(isinstance(arg, dict) for arg in args)
        list_in = any(isinstance(arg, list) for arg in args)
        if len(args) == 2 and not dict_in :
            well, value, *trash = args
        #add_values
        if len(args) == 1 and dict_in:
            well, *trash = args
            value = None
       #multi_value
        if len(args) == 2 and list_in:
            well, value, *trash = args
        return well, value                             
           

    def add_value(self, *args):
        """
        add a value to one given well position (eg : 'A1', 'test 1')
        
        :param str well: 'A1' => On row A in column 1 add a value
        :param str value: 'test 1' => value to add on selected well
        :return: np.array([[0, 1, 2, 3],
                           [A, 'test 1', 0, 0],
                           [B, 0, 0, 0]])
        """
        well, value = self._args_analyse(*args)
        self._eval_well(BioPlateMatrix(well), value)
        #row, column = BioPlateMatrix(well)
        #self[row, column] = value
        return self

    def add_value_row(self, *args):
        """
        add value to a given row on a list of column (eg : 'A[2,3]', 'test 2')
        
        :param wells: 'A[2,3]' => On row A add value from column 2 to 3 included
        :param value: 'test 2' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 2', 'test 2'],
                           [B, 0, 0, 0]])
        """
        well, value = self._args_analyse(*args)
        #dimension, row, col_start, col_end = BioPlateMatrix(well)
        #self[row, col_start:col_end] =value
        self._eval_well(BioPlateMatrix(well), value)
        return self

    def add_value_column(self, *args):
        """
        addvalue to a given column on a list of row (eg : '2[A-B]', 'test 3')
        
        :param wells: '2[A-B]' => On column 2 add value from row A to B included
        :param value: 'test 3' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 3', 0],
                           [B, 0, 'test 3', 0]])
        """
        well, value = self._args_analyse(*args)
        #dimension, row_start, row_end, column = BioPlateMatrix(well)
        #self[row_start:row_end, column] = value
        self._eval_well(BioPlateMatrix(well), value)
        return self

    def add_values(self, *args):
        """
        parse dictionaries of multiple value to add with keys are wells and values are value
        
        (eg : {'A1' : 'test 4', 'B3' : 'test 5'})
        :param values: {'A1' : 'test 4', 'B3' : 'test 5'}
        :eturn: plate
        """
        well_dict, *trash = self._args_analyse(*args)
        try:
            Eval = lambda W_V : self._eval_well_value(W_V[0], W_V[1])
            list(map(Eval, well_dict.items()))
            return self
        except AttributeError:
            return f"{type(well_dict)} is a wrong format, dictionary should be used"

    """
    def add_multi_value(self, *args):
        
        parse an add_value_row or column in a compact manner and pass it to evaluate(eg : 'A-C[1-5]', ['val1' , 'val2', 'val3'])
        
        :param multi_wells: 'A-C[1-5]' => On row A, B and C add value from column 1 to 5 included
        :param values: ['val1' , 'val2', 'val3'] => On row A add value 'val1', on row B add value 'val2' from column 1 to 5
        :return: plate
        
        multi_wells, values = self._args_analyse(*args)
        wells = BioPlateMatrix(multi_wells)
        if len(wells) != len(values):
            raise ValueError(f"missmatch between wells ({len(wells)}) and values ({len(values)})")
        self._eval_well_value(multi_wells, values)
        return self
    """
    def evaluate(self, *args):
        """
        set a value 
        """
        well, value, *trash = self._args_analyse(*args)
        if isinstance(well, dict):
            self.add_values(*args)
            return self
        self._eval_well_value(well, value)
        return self

    def _eval_well(self, well, value=None):
        """
        well = ("All", "R", 2) => self[:,well[2]]
        well = ("All", "C", 2) => self[well[2]]
        well = ("R", 2, 6, 4) => self[well[1]:well[2], well[3]]
        well = ("C", 2, 6, 8) => self[well[1],well[2]: well[3]]
        """
        if well[0] == "R":
            if value is not None:
                self[well[1]:well[2], well[3]] = value
            else:
                return self[well[1]:well[2], well[3]]
        elif well[0] == "C":
            if value is not None:
                self[well[1], well[2]:well[3]] = value
            else:
                return self[well[1], well[2]:well[3]]
        elif well[0] == "All":
             if well[1] == "R":
                 if value is not None:
                     self[1:,1:][well[2]] = value
                 else:
                     return self[1:,1:][well[2]]
             elif well[1] == "C":
                 if value is not None:
                     self[1:,1:][:,well[2]] = value
                 else:
                     return self[1:,1:][:,well[2]]
        else:
            if value is not None:
                self[well[0], well[1]] = value
            else:
                 return self[well[0], well[1]]

    def _eval_well_value(self, well, value):
        well = BioPlateMatrix(well)
        if isinstance(well, list):
            if len(well) == len(value):
                for w, v in zip(well, value):             
                    self._eval_well(w,v)
        else:           
            self._eval_well(well, value)

    def get(self, *well):
        if len(well) > 1:
            test = lambda x : list(x) if not isinstance(x, str) else x
            return list(map(test, list(map(self._eval_well, map(BioPlateMatrix, well)))))
        else:
            return self._eval_well(BioPlateMatrix(well[0]))

    def save(self, plate, plate_name, **kwargs):
        dbName = kwargs.get("db_hist_name")
        if not dbName :
            phi = PlateHist()
        else:
            phi = PlateHist(db_name=dbName)
        if isinstance(plate, list):
            well = next(self.__iterate(plate[0], Ovalue=True)).shape
        else:
            well = next(self.__iterate(plate, Ovalue=True)).shape
        numWell = well[0] * well[1]
        response = phi.add_hplate(numWell, plate_name, plate)
        if isinstance(response, str):
            return response
        elif isinstance(response, int):
            dict_update = {"plate_name": plate_name,
                           "plate_array": plate}
            return phi.update_hplate(dict_update, response, key="id")

    def table(self, headers="firstrow", *args, **kwargs):
        """
        return a tabulate object of plate.array
        
        :param plate: numpy.array of a plate object
        :param kwargs: keys arguments use by tabulate function
        :return:
        """
        if not args:
            return tabulate(self, headers=headers, **kwargs)
        
    def iterate(self, order="C", accumulate=True):
        yield from self._iterate(self, order=order, accumulate=accumulate)
    
    
    def _iterate(self, *plates, order="C", accumulate=True):
        """
        generator return [well, value]
        
        :param plate: numpy.array of plate object
        :param order: iterate by column C or by row R
        """
        Order = {"C" : "F", "R" : "C"}
        if accumulate:
            row, column, values = self._acumul_iterate(*plates)
            for r, c, *v in np.nditer((row, column) + values, order=Order[order]):
                yield (self._merge_R_C_(r, c),) + tuple(map(str, v))
        else:
            for row, column, value  in self.__iterate(*plates):
                for r, c, v in np.nditer((row, column, value), order=Order[order]):
                    yield (self._merge_R_C_(r, c), str(v))
        
    def _acumul_iterate(self, *plates):
        values = []
        for row, column, value  in self.__iterate(*plates):
             values.append(value)
        return row, column, tuple(values)
         
    def __iterate(self, *plates, Ovalue=False):
        for plate in plates:
            if len(plate.shape) == 2:
                yield from self.___iterate(plate, Ovalue=Ovalue)
            else:
                 for pl in plate:
                     yield from self.___iterate(pl, Ovalue=Ovalue)
                     
    def ___iterate(self, plate, Ovalue=False):
            columns = plate[0,1:]
            rows = plate[1:, 0:1]
            values = plate[1:, 1:]
            if Ovalue:
                yield values
            else:
                yield rows, columns, values
            
    def _merge_R_C_(self, row, column):
      RC =   "".join(map(str, [row, column]))
      return RC    

    def count(self, reverse=False):
        return self._count(self, reverse=reverse)

    def __count(self, plate, reverse=False):
        """

        :param plate:
        :return:
        """
        #for values in self.__iterate(*plates, Ovalue=True):
        unique, count = np.unique(plate, return_counts=True)
        count_in_dict = dict(zip(unique, count))
        count_in_dict = dict(sorted(count_in_dict.items(), key=lambda x:x[1], reverse=reverse))
        return count_in_dict

    def _count(self, *plates, reverse=False):
        """

        :param plate:
        :return:
        """
        nb_plate = len(plates)
        multi = nb_plate > 1
        insert =  len(plates[0].shape) > 2
        if multi or insert:
            results = {}
            n = 0
            y = 0
            for values in self.__iterate(*plates, Ovalue=True):
                Count = self.__count(values, reverse=reverse)
                if insert and multi: # a stack of Insert plate
                    mod = y % 2
                    y += 1
                    if mod == 0:
                        inter = {}
                        inter["top"] = Count
                    else:
                        inter["bot"] = Count
                        results[n] = inter
                        n += 1
                elif insert: # insert plate only
                    if n == 0:
                        results["top"] = Count
                        n += 1
                    else:
                         results["bot"] = Count
                else: # Stack of simple plate
                    results[n] = Count
                    n += 1
        else: # a single plate
        	results = self.__count(next(self.__iterate(*plates, Ovalue=True)), reverse=reverse)
        return results

