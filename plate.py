import ast
import re
import string
import numpy as np
import time

from tabulate import tabulate
from database.plate_db import get_plate

"""
    add value : add value to one wells (eg : 'B5)
    add_value_row : add the same values on multiple row (eg: 'C[3,12]', 'test')
    add_value_column : add the same values on multiple column (eg: '3[A,H]', 'test4')

"""


class Plate:
    "A row is symbolise by it's letter, a column by a number"


    def __init__(self, args, key='numWell'):
        "plates number of well : [column, row]"
        #self.plates = {6 : [3, 2], 12 : [4, 3], 24 : [6, 4], 96 : [12, 8]}
        self.plates = get_plate(args, key=key)[0]
        """
        if re.search("^\d+", str(numWell)):
            self.NumWell = NumWell
        elif re.search("\[\d+,", str(NumWell)):
            column, row = NumWell[0], NumWell[1]
            self.NumWell= int(column) * int(row)
            self.plates[self.NumWell] = [column, row]
        """
        self.letter = np.array(list(string.ascii_uppercase))
        self.plate1 = self.plate_array1

    @property
    def plate_array1(self):
        plate_representation = np.zeros([self.plates.numRows + 1, self.plates.numColumns + 1], dtype='U40')
        plate_representation[0] = np.array([x for x in range(self.plates.numColumns+1)])
        for i in range(self.plates.numRows):
            z = i + 1
            plate_representation[z][0] = self.letter[i]
        return plate_representation

    def matrix_well(self, well):
        "return row column as index of plate"
        row, column = filter(None, re.split('(\d+)' ,well))
        row = self.well_letter_index(row)
        return row, int(column)

    def add_value1(self, well, value):
        "add a value to a given well position eg : 'A1'"
        plate = self.plate1
        row, column = self.matrix_well(well)
        plate[row, column] = value
        self.plate1 = plate
        return plate

    def add_value_row1(self, wells, value):
        "wells = row[start,stop]"
        plate = self.plate1
        row, l= list(filter(None, re.split('(\[\d+,\d+,?\d?\])', wells.replace(" ",""))))
        row = self.well_letter_index(row)
        column = ast.literal_eval(l)
        column if len(column) == 3 else column.append(1)
        if column[0] == 0:
            print("can't assign value on 0")
            return
        else :
            plate[row, column[0]:column[1]+1] = value
            self.plate1 = plate
            return plate

    def add_value_column1(self, wells, value):
        "wells = column[start letter, stop letter, step number]"
        plate = self.plate1
        column, row = list(filter(None, re.split('(\d+)' ,wells.replace(" ",""))))
        row = list(row)
        """
        try:
            step = int(row[5]) if row[5] else 1
        except:
            step = 1
        """
        row_start = self.well_letter_index(row[1])
        row_end = self.well_letter_index(row[3]) + 1
        plate[row_start:row_end, int(column)] = value
        self.plate1 = plate
        return plate

    def add_values1(self, values):
        "values is a dict with keys are position and values are value"
        for key, value in values.items():
            self.evaluate1(key, value)
        return self.plate1

    def add_multi_value1(self, multi_wells, values):
        "multi_wells = 'A-C[1-5]', values = ['val1' , 'val2', 'val3']"
        wells = self.multi_row_column(multi_wells)
        if len(wells) == len(values):
            for well, value in zip(wells, values):
                self.evaluate1(well, value)

    def evaluate1(self, wells, value):
        "select the right function too add value on wells format (column[], row[], row column)"
        if re.search("^(\d+\[)", wells):
            return self.add_value_column1(wells, value)
        elif re.search("^([A-Za-z]\[)", wells):
            return self.add_value_row1(wells, value)
        elif re.search("[A-Za-z]\d+", wells):
            return self.add_value1(wells, value)
        elif re.search("^[A-Za-z]-[A-Za-z]|^\d+?-\d+?", wells):
            self.add_multi_value1(wells, value)
        else:
            return None

    def well_letter_index(self, row_letter):
        row_index = np.searchsorted(self.letter, row_letter) + 1
        return row_index
        
    def letter_index(self, letter):
        index = np.searchsorted(self.letter, letter)
        return index

    def multi_row_column(self, multi_wells):
        "return à list of well également : 'A-E[1,5]' or '1-5[A,E]'"
        results = []
        if re.search("^[A-Za-z]-[A-Za-z]", multi_wells):
            letter = list(filter(None, re.split('(\w)' ,multi_wells.replace(" ",""))))
            letter_start = self.letter_index(letter[0]) 
            letter_end = self.well_letter_index(letter[2])
            a = ''.join(letter[3:]) 
            for i in range(letter_start, letter_end):
                results.append(''.join([self.letter[i], a]))
            print('1 : ', results)
            return results
        elif re.search("\d+?-\d+?", multi_wells):
            column = list(filter(None, re.split('(\w+)' ,multi_wells.replace(" ",""))))
            column_start = int(column[0]) 
            column_end = int(column[2])
            a = ''.join(column[3:])
            for i in range(column_start, column_end + 1):
                results.append(''.join([str(i), a]))
            print('2 : ',results)
            return results

    def table(self, plate, **kwargs):
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
    Plate.add_value1('E5', 'test3')
    Plate.add_value_row1('C[3,12]', 'test')
    Plate.add_value_column1('3[A,H]', 'test4')
    Plate.add_values1(v)
    print(Plate.table(Plate.plate1))
    time_2= int(round(time.time() * 1000))
    print(f'numpy run in : {(time_2 - time_1)}')

    
