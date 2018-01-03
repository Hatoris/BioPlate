import ast
import re
import string
import time


import numpy as np
from tabulate import tabulate
from BioPlate.database.plate_db import get_plate

"""
    add value : add value to one wells (eg : 'B5)
    add_value_row : add the same values on multiple row (eg: 'C[3,12]', 'test')
    add_value_column : add the same values on multiple column (eg: '3[A,H]', 'test4')
    '1-3[B,E]' == '1[B,E]', '2[B,E]', '3[B,E]' == 'B1', 'C1', 'D1', 'E1', 'B2', 'C2' ... == '1B', '1C' ... 
    ---------     ----------------------------    --------------------------------------------------------
    condensed             medium                                       small                              : form assignation

"""


class Plate:
    """A row is symbolise by it's letter, a column by a number"""

    def __init__(self, args, key='numWell'):
        """
        :param args: value to search in databse
        :param key: column to search args, by default column is numWell
        """
        self.plates = get_plate(args, key=key)[0]
        self.letter = np.array(list(string.ascii_uppercase))
        self.plate = self.plate_array

    @property
    def plate_array(self):
        """
        get a numpy.array representation of a plate in dtype='U40' (eg : 6 wells plate)
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 0, 0],
                           [B, 0, 0, 0]])
        """
        plate_representation = np.zeros([self.plates.numRows + 1, self.plates.numColumns + 1], dtype='U40')
        plate_representation[0] = np.array([x for x in range(self.plates.numColumns+1)])
        for i in range(self.plates.numRows):
            z = i + 1
            plate_representation[z][0] = self.letter[i]
        return plate_representation

    def matrix_well(self, well):
        """
        return row column as index of plate (eg: 'A1')
        :param well: 'A1' => position of well to get 2D index
        :return: tuple of (row, column) (eg : (1, 1))
        """
        if re.search("^([A-Za-z]\d+)", well):
            row, column = filter(None, re.split('(\d+)' ,well))
            row = self.well_letter_index(row)
            return row, int(column)
        elif re.search("^(\d+[A-Za-z])", well):
            column, row = filter(None, re.split('(\d+)' ,well))
            row = self.well_letter_index(row)
            return row, int(column)

    def add_value(self, well, value):
        """
        add a value to one given well position (eg : 'A1', 'test 1')
        :param well: 'A1' => On row A in column 1 add a value
        :param value: 'test 1' => value to add on selected well
        :return: np.array([[0, 1, 2, 3],
                           [A, 'test 1', 0, 0],
                           [B, 0, 0, 0]])
        """
        plate = self.plate
        row, column = self.matrix_well(well)
        plate[row, column] = value
        self.plate = plate
        return plate

    def add_value_row(self, wells, value):
        """
        add value to a given row on a list of column (eg : 'A[2-3]', 'test 2')
        :param wells: 'A[2-3]' => On row A add value from column 2 to 3 included
        :param value: 'test 2' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 2', 'test 2'],
                           [B, 0, 0, 0]])
        """
        plate = self.plate
        row, l= list(filter(None, re.split('(\[\d+,\d+,?\d?\])', wells.replace(" ",""))))
        row = self.well_letter_index(row)
        column = ast.literal_eval(l)
        column if len(column) == 3 else column.append(1)
        if column[0] == 0:
            print("can't assign value on 0")
            return
        else :
            plate[row, column[0]:column[1]+1] = value
            self.plate = plate
            return plate

    def add_value_column(self, wells, value):
        """
        add value to a given column on a list of row (eg : '2[A-B]', 'test 3')
        :param wells: '2[A-B]' => On column 2 add value from row A to B included
        :param value: 'test 3' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 3', 0],
                           [B, 0, 'test 3', 0]])
        """
        plate = self.plate
        column, row = list(filter(None, re.split('(\d+)' ,wells.replace(" ",""))))
        row = list(row)
        row_start = self.well_letter_index(row[1])
        row_end = self.well_letter_index(row[3]) + 1
        plate[row_start:row_end, int(column)] = value
        self.plate = plate
        return plate

    def add_values(self, values):
        """
        parse dictionaries of multiple value to add with keys are wells and values are value
        (eg : {'A1' : 'test 4', 'B3' : 'test 5'})
        :param values: {'A1' : 'test 4', 'B3' : 'test 5'}
        :return: plate
        """
        for key, value in values.items():
            self.evaluate(key, value)
        return self.plate

    def add_multi_value(self, multi_wells, values):
        """
        parse an add_value_row or column in a compact manner and pass it to evaluate(eg : 'A-C[1-5]', ['val1' , 'val2', 'val3'])
        :param multi_wells: 'A-C[1-5]' => On row A, B and C add value from column 1 to 5 included
        :param values: ['val1' , 'val2', 'val3'] => On row A add value 'val1', on row B add value 'val2' from column 1 to 5
        :return: plate
        """
        wells = self.multi_row_column(multi_wells)
        if len(wells) == len(values):
            for well, value in zip(wells, values):
                self.evaluate(well, value)
        else:
            print(f"for {wells} = {values} Number of wells are {len(wells)} and number of values are {len(values)}")
        return self.plate

    def evaluate(self, wells, value):
        """
        select the right function to add value (eg : 'A[1,3]' or '1-3[A,B]', ['val1', 'val2', 'val3'])
        :param wells: '1-3[A,B]' => On column 1, 2 and 3 add value from row A to B included
        :param value: ['val1' , 'val2', 'val3'] => On column 1 add value 'val1', on column 2 add value 'val2' from row A to B
        :return: plate or None
        """
        if re.search("^(\d+\[)", wells):
            return self.add_value_column(wells, value)
        elif re.search("^([A-Za-z]\[)", wells):
            return self.add_value_row(wells, value)
        elif re.search("[A-Za-z]\d+", wells):
            return self.add_value(wells, value)
        elif re.search("^[A-Za-z]-[A-Za-z]|^\d+?-\d+?", wells):
            return self.add_multi_value(wells, value)
        else:
            return None

    def well_letter_index(self, row_letter):
        """
        get index for a given letter (eg : C)
        :param row_letter: C => letter of a row
        :return: 3 => index of row C in plate.array
        """
        row_index = np.searchsorted(self.letter, row_letter) + 1
        return row_index
        
    def letter_index(self, letter):
        """
        get index of a given letter in the numpy.array
        :param letter: C => letter of interest
        :return: 2 => index of letter C in letter.array
        """
        index = np.searchsorted(self.letter, letter)
        return index

    def multi_row_column(self, multi_wells):
        """
        split condensed wells assignation on medium form (eg : 'A-E[1,5]' or '1-5[A,E]')
        :param multi_wells: 'A-E[1,5]' => On row A, B, C, D and E add value from column 1 to 5 included
        :return: ['A[1,5]', 'B[1,5]', 'C[1,5]', 'D[1,5]', 'E[1,5]'] => medium form of the condensed one 'A-E[1,5]'
        """
        results = []
        if re.search("^[A-Za-z]-[A-Za-z]", multi_wells):
            letter = list(filter(None, re.split('(\w)' ,multi_wells.replace(" ",""))))
            letter_start = self.letter_index(letter[0])
            letter_end = self.well_letter_index(letter[2])
            a = ''.join(letter[3:])
            for i in range(letter_start, letter_end):
                results.append(''.join([self.letter[i], a]))
            return results
        elif re.search("\d+?-\d+?", multi_wells):
            column = list(filter(None, re.split('(\w+)' ,multi_wells.replace(" ",""))))
            column_start = int(column[0]) 
            column_end = int(column[2])
            a = ''.join(column[3:])
            for i in range(column_start, column_end + 1):
                results.append(''.join([str(i), a]))
            return results

    def table(self, plate, **kwargs):
        """
        return a tabulate object of plate.array
        :param plate: numpy.array of a plate object
        :param kwargs: keys arguments use by tabulate function
        :return:
        """
        return tabulate(plate, headers='firstrow', **kwargs)
        
   

if __name__ == '__main__':



    #print(Plate.plates)
    #print(re.split('(\d+)' ,'C12')) 
    #print(Plate.table(Plate.plate))
    #print(Plate.matrix_well('A2'))
    #print(Plate.matrix_well('B3'))
    #print(Plate.table(Plate.add_value('B3', 'test')))
    #print(Plate.add_value_row('C[3,12]', 'test'))
    #print(Plate.table(Plate.add_value_row('C[3,12]', 'test')))
    # print(Plate.table(Plate.plate))
    # Plate.add_value_row('B[2 ,8,2]', 'test2')
    #print(Plate.table(Plate.plate))
    #Plate.evaluate('3[C,E]', 'test5')
    #print(len(Plate.plate[1]), len(Plate.plate[2]))
    #print(Plate.table(Plate.plate))
    #print(Plate.table(Plate.plate))
    #print(Plate.multi_row_column('A-E[1-5]'))
    #Plate.add_multi_value('A-C[1,5]', ['test1', 'test2', 'test3'])
    #Plate.add_multi_value('6-8[A,F]', ['test1', 'test2', 'test3'])

    v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'], 'E-G[8,10]' : ['Val1', 'Val2', 'Val3']}

    #numpy
    time_1 = int(round(time.time() * 1000))
    time.sleep(0.01)
    Plate = Plate(96)
    Plate.add_value('E5', 'test3')
    Plate.add_value('10A', 'test5')
    Plate.add_value_row('C[3,12]', 'test')
    Plate.add_value_column('3[A,H]', 'test4')
    Plate.add_values(v)
    print(Plate.table(Plate.plate))
    time_2= int(round(time.time() * 1000))
    print(f'numpy run in : {(time_2 - time_1)}')

    
