from tabulate import tabulate
import string
import re
import ast
from database.plate_db import create_plate_db

"""
TODO: add sqlite3 for plates information add surface and volume too

"""

class plate:
    "A row is symbolise by it's letter, a column by a number" 
    
    def __init__(self, DB, NumWell):
        "plates number of well : [column, row]"
        self.plates = {6 : [3, 2], 12 : [4, 3], 24 : [6, 4], 96 : [12, 8]}
        if re.search("^\d+", str(NumWell)):
            self.NumWell = NumWell
        elif re.search("\[\d+,", str(NumWell)):
            column, row = NumWell[0], NumWell[1]
            self.NumWell= int(column) * int(row)
            self.plates[self.NumWell] = [column, row]
        self.letter = list(string.ascii_uppercase)
        self.plate = self.plate_array
        
    @property
    def plate_array(self):
        "return a nested array representation of plate" 
        plate = []
        column = [x for x in range(self.plates[self.NumWell][0]+1)]
        plate.append(column)
        for i in range(self.plates[self.NumWell][1]):
            row = [''] * (len(column) - 1) 
            row.insert(0, self.letter[i])
            plate.append(row)
        return plate
        
      
    def add_value(self, well, value):
        "add a value to a given well position eg : 'A1'" 
        plate = self.plate
        row, column = self.matrix_well(well)
        plate[row].insert(column, value)
        self.plate = plate
        return plate
        
    def add_value_row(self, wells, value):
        "wells = row[start,stop,step]"
        plate = self.plate
        row, l= list(filter(None, re.split('(\[\d+,\d+,?\d?\])' ,wells.replace(" ","")))) 
        row = self.well_letter_index(row)
        val = ast.literal_eval(l)
        val if len(val) == 3 else val.append(1)
        if val[0] == 0:
            print("can't assign value on 0")
            return
        for i in range(val[0], val[1]+1, val[2]):
            plate[row][i] = value
        self.plate = plate
        return plate
        
    def add_value_column(self, wells, value):
        "wells = column[start letter, stop letter, step number]" 
        column, row = list(filter(None, re.split('(\d+)' ,wells.replace(" ",""))))
        row = list(row)
        try:
            step = int(row[5]) if row[5] else 1
        except:
            step = 1
        start = self.well_letter_index(row[1])
        end = self.well_letter_index(row[3]) + 1
        for row in range(start, end, step):
            self.plate[row][int(column)] = value
        
    def add_multi_value(self, multi_wells, values):
        "multi_wells = 'A-C[1-5]', values = ['val1' , 'val2', 'val3']" 
        wells = self.multi_row_column(multi_wells)
        if len(wells) == len(values):
            for well, value in zip(wells, values):
                self.evaluate(well, value)
        
        
    def add_values(self, values):
        "values is a dict with keys are position and values are value" 
        for key, value in values.items():
            self.evaluate(key, value)
        return self.plate
        
    def evaluate(self, wells, value):
        "select the right function too add value on wells format (column[], row[], row column)" 
        if re.search("^(\d+\[)", wells):
            return self.add_value_column(wells, value) 
        elif re.search("^([A-Za-z]\[)", wells):
            return self.add_value_row(wells, value) 
        elif re.search("[A-Za-z]\d+", wells):
            return self.add_value(wells, value)
        elif re.search("^[A-Za-z]-[A-Za-z]|^\d+?-\d+?", wells):
            self.add_multi_value(wells, value) 
        else:
            return None
        
    def matrix_well(self, well):
        "return row column as index of plate" 
        row, column = filter(None, re.split('(\d+)' ,well)) 
        row = self.well_letter_index(row) 
        return row, int(column)
        
    def well_letter_index(self, row_letter):
        row_index = self.letter.index(row_letter) + 1
        return row_index
        
    def letter_index(self, letter):
        index = self.letter.index(letter)
        return index
        
    def multi_row_column(self, multi_wells):
        "return à list of well également : 'A-E[1,5]' or '1-5[A,E]'"
        results = []
        if re.search("^[A-Za-z]-[A-Za-z]", multi_wells):
            print(multi_wells) 
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
    
    def table(self, Plate):
        return tabulate(Plate, headers='firstrow') 
        
   

if __name__ == '__main__':

    Plate = plate([24,16])
    print(Plate.plates)
    #print(re.split('(\d+)' ,'C12')) 
    #print(Plate.table(Plate.plate))
    #print(Plate.matrix_well('A2'))
    #print(Plate.matrix_well('B3'))
    #Plate.add_value('E5', 'test3')
    #print(Plate.table(Plate.add_value('B3', 'test')))
    #print(Plate.add_value_row('C[3,12]', 'test'))
    #print(Plate.table(Plate.add_value_row('C[3,12]', 'test')))
    #Plate.add_value_row('C[3,12]', 'test')
    #print(Plate.table(Plate.plate))
    #Plate.add_value_row('B[2 ,8,2]', 'test2')
    #Plate.add_value_column('3[A,H]', 'test4')
    #print(Plate.table(Plate.plate))
    #Plate.evaluate('3[C,E]', 'test5')
    #print(len(Plate.plate[1]), len(Plate.plate[2]))
    #print(Plate.table(Plate.plate))
    v = {'A[2,8]' : 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2']}
    Plate.add_values(v)
    #print(Plate.table(Plate.plate))
    #print(Plate.multi_row_column('A-E[1-5]'))
    #Plate.add_multi_value('A-C[1,5]', ['test1', 'test2', 'test3'])
    #Plate.add_multi_value('6-8[A,F]', ['test1', 'test2', 'test3'])
    print(Plate.table(Plate.plate))
