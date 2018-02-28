import ast
import re
import time
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
        row, column = BioPlateMatrix(well)
        self[row, column] = value
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
        dimension, row, col_start, col_end = BioPlateMatrix(well)
        self[row, col_start:col_end] =value
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
        dimension, row_start, row_end, column = BioPlateMatrix(well)
        self[row_start:row_end, column] = value
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

    def add_multi_value(self, *args):
        """
        parse an add_value_row or column in a compact manner and pass it to evaluate(eg : 'A-C[1-5]', ['val1' , 'val2', 'val3'])
        
        :param multi_wells: 'A-C[1-5]' => On row A, B and C add value from column 1 to 5 included
        :param values: ['val1' , 'val2', 'val3'] => On row A add value 'val1', on row B add value 'val2' from column 1 to 5
        :return: plate
        """
        multi_wells, values = self._args_analyse(*args)
        wells = BioPlateMatrix(multi_wells)
        self._eval_well_value(multi_wells, values)
        return self

    def evaluate(self, *args):
        well, value, *trash = self._args_analyse(*args)
        print(well)
        if isinstance(well, dict):
            self.add_values(*args)
            return self
        self._eval_well_value(well, value)
        return self

    def __eval_well_value(self, well, value):
        """
        eval well and add value to self, try to see if we can get generator 
        """
        if well[0] == "R":
            self[well[1]:well[2], well[3]] = value
        elif well[0] == "C":
            self[well[1], well[2]:well[3]] = value
        else:
             self[well[0], well[1]] = value

    def _eval_well_value(self, well, value):
        well = BioPlateMatrix(well)
        if isinstance(well, list):
            if len(well) == len(value):
                for w, v in zip(well, value):
                    self.__eval_well_value(w, v)
        else:
            self.__eval_well_value(well, value)




    def save(self, plate_name, db_hist_name=None):
        if not db_hist_name:
            phi = PlateHist()
        else:
            phi = PlateHist(db_name=db_hist_name)
        response = phi.add_hplate(self.plates.numWell, plate_name, self.plate, Plate_id=self.plates.id)
        if isinstance(response, str):
            return response
        elif isinstance(response, int):
            dict_update = {"plate_name": plate_name,
                           "plate_array": self.plate}
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
         
    def __iterate(self, *plates):
        for plate in plates:
            columns = plate[0,1:]
            rows = plate[1:, 0:1]
            values = plate[1:, 1:]
            yield rows, columns, values
            
    def _merge_R_C_(self, row, column):
      RC =   "".join(map(str, [row, column]))
      return RC
    
    def ____iterate(self, order="C", acumulate=True):
        """

        :param order:
        :aram acumulate:
        :return:
        """
        yield from self.iter_evaluate(self, order=order, acumulate=acumulate)

    def count(self, plate):
        """

        :param plate:
        :return:
        """
        unique, count = np.unique(plate[1:,1:], return_counts=True)
        count_in_dict = dict(zip(unique, count))
        return count_in_dict

    def count_elements(self, plate):
        """

        :param plate:
        :return:
        """
        dim = bpu.dimension(plate)
        if dim:
            results = {}
            n = 0
            for p in plate:
                results[n] = self.count(p)
                n += 1
        else:
        	results = self.coun(plate)
        return results

    def counts(self):
        """

        :return:
        """
        return self.count_elements(self.plate)


if __name__ == "__main__":
    bpm = BioPlateManipulation()
    #print(bpm.split_multi_row_column("1-8[A,C]"))
   # print(bpm.split_multi_row_column("A-G[1,8]"))