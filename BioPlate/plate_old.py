import ast
import re
import time

import numpy as np
from string import ascii_uppercase
from tabulate import tabulate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.utilitis import dimension

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

    def __init__(self, args, key='numWell', db_name=None):
        """
        :param args: value to search in database
        :param key: column to search args, by default column is numWell
        """
        if not db_name:
            pdb = PlateDB()
        else:
            pdb = PlateDB(db_name=db_name)
        self.plates = pdb.get_one_plate(args, key=key)
        self.letter = np.array(list(ascii_uppercase))
        self.plate = self.plate_array

    @property
    def plate_array(self):
        """
        get a numpy.array representation of a plate in dtype='U40' (eg : 6 wells plate)
        
        :return: np.array([[0, 1, 2, 3], [A, 0, 0, 0], [B, 0, 0, 0]])
        """
        plate_representation = np.zeros([self.plates.numRows + 1, self.plates.numColumns + 1], dtype='U40')
        plate_representation[0] = np.array([x for x in range(self.plates.numColumns + 1)])
        for i in range(self.plates.numRows):
            z = i + 1
            plate_representation[z][0] = self.letter[i]
        plate_representation[0][0] = ' '
        return plate_representation

    def matrix_well(self, well):
        """
        return coordonates (row, column) as index of plate (eg: 'A1')
        
        :param str well: coordonate of a well (eg,:'A1')
        :return: tuple of (row, column) (eg : (1, 1))
        """
        if re.search("^([A-Za-z]\d+)", well):
            row, column = filter(None, re.split('(\d+)', well))
            row = self.well_letter_index(row)
            return row, int(column)
        elif re.search("^(\d+[A-Za-z])", well):
            column, row = filter(None, re.split('(\d+)', well))
            row = self.well_letter_index(row)
            return row, int(column)

    def add_value(self, well, value):
        """
        add a value to one given well position (eg : 'A1', 'test 1')
        
        :param str well: 'A1' => On row A in column 1 add a value
        :param str value: 'test 1' => value to add on selected well
        :return: np.array([[0, 1, 2, 3],
                           [A, 'test 1', 0, 0],
                           [B, 0, 0, 0]])
        """
        row, column = self.matrix_well(well)
        self.plate[row, column] = value
        return self.plate

    def add_value_row(self, wells, value):
        """
        add value to a given row on a list of column (eg : 'A[2,3]', 'test 2')
        
        :param wells: 'A[2,3]' => On row A add value from column 2 to 3 included
        :param value: 'test 2' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 2', 'test 2'],
                           [B, 0, 0, 0]])
        """
        row, l = list(filter(None, re.split('(\[\d+\,\d+])|(\[\d+\-\d+\])', wells.replace(" ", ""))))
        row = self.well_letter_index(row)
        l = l.replace("-", ",")
        column = sorted(ast.literal_eval(l))
        if column[0] == 0:
            return "can't assign value on 0"
        else:
            self.plate[row, column[0]:column[1] + 1] = value
            return self.plate

    def add_value_column(self, wells, value):
        """
        add value to a given column on a list of row (eg : '2[A-B]', 'test 3')
        
        :param wells: '2[A-B]' => On column 2 add value from row A to B included
        :param value: 'test 3' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 3', 0],
                           [B, 0, 'test 3', 0]])
        """
        column, row = list(filter(None, re.split('(\d+)', wells.replace(" ", ""))))
        row = sorted(list(row))
        row_start = self.well_letter_index(row[1])
        row_end = self.well_letter_index(row[2]) + 1
        self.plate[row_start:row_end, int(column)] = value
        return self.plate

    def add_values(self, values):
        """
        parse dictionaries of multiple value to add with keys are wells and values are value
        
        (eg : {'A1' : 'test 4', 'B3' : 'test 5'})
        :param values: {'A1' : 'test 4', 'B3' : 'test 5'}
        :return: plate
        """
        try:
            for key, value in values.items():
                self.evaluate(key, value)
            return self.plate
        except AttributeError:
            return f"{type(values)} is a wrong format, dictionary should be used"

    def add_multi_value(self, multi_wells, values):
        """
        parse an add_value_row or column in a compact manner and pass it to evaluate(eg : 'A-C[1-5]', ['val1' , 'val2', 'val3'])
        
        :param multi_wells: 'A-C[1-5]' => On row A, B and C add value from column 1 to 5 included
        :param values: ['val1' , 'val2', 'val3'] => On row A add value 'val1', on row B add value 'val2' from column 1 to 5
        :return: plate
        """
        wells = self.split_multi_row_column(multi_wells)
        if len(wells) == len(values):
            for well, value in zip(wells, values):
                self.evaluate(well, value)
        else:
            raise ValueError(
                f"for {wells} = {values} Number of wells are {len(wells)} and number of values are {len(values)}")
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
        elif re.search("([A-Za-z]\d+)|(\d+[A-Za-z])", wells):
            return self.add_value(wells, value)
        elif re.search("([A-Za-z]\-[A-Za-z]\[)|(\d+\-\d+\[)", wells):
            return self.add_multi_value(wells, value)
        else:
            raise SyntaxError(f"Can't find a match pattern in this {wells}")

    def well_letter_index(self, row_letter):
        """
        get index for a given letter (eg : C)
        
        :param row_letter: C => letter of a row
        :return: 3 => index of row C in plate.array
        """
        return np.searchsorted(self.letter, row_letter) + 1

    def letter_index(self, letter):
        """
        get index of a given letter in the numpy.array
        
        :param letter: C => letter of interest
        :return: 2 => index of letter C in letter.array
        """
        return np.searchsorted(self.letter, letter)

    def index_letter(self, index_letter):
        """
        return letter of define index
        :param index_letter: 2 => index of interest
        :return: C => letter of a given index
        """
        return self.letter[index_letter]

    def split_multi_row_column(self, multi_wells):
        """
        split condensed wells assignation on medium form (eg : 'A-E[1,5]' or '1-5[A,E]')
        
        :param multi_wells: 'A-E[1,5]' => On row A, B, C, D and E add value from column 1 to 5 included
        :return: ['A[1,5]', 'B[1,5]', 'C[1,5]', 'D[1,5]', 'E[1,5]'] => medium form of the condensed one 'A-E[1,5]'
        """
        # Common to row and column
        results = []
        infos = sorted(list(filter(None, re.split('(\W)', multi_wells.replace(" ", "")))))
        to_add = ["[", ",", "]"]
        if re.search("([A-Za-z]-[A-Za-z]\[)", multi_wells):
            val = "row"
        elif re.search("(\d+\-\d+\[)", multi_wells):
            val = "column"
        else:
            val = None
            raise SyntaxError(f"Can't find a match pattern in this {multi_wells}")
        # Dictionarie of row and column specific informations
        start = {"row": self.letter_index(infos[4]), "column": int(infos[2])}
        end = {"row": self.well_letter_index(infos[5]), "column": int(infos[3]) + 1}
        position_1 = {"row": infos[2], "column": infos[4]}
        position_3 = {"row": infos[3], "column": infos[5]}
        value = {"row": self.index_letter, "column": str}

        # Common transformation to row and column
        to_add.insert(1, str(position_1[val]))
        to_add.insert(3, str(position_3[val]))
        a = ''.join(to_add)
        for i in range(start[val], end[val]):
            results.append(''.join([value[val](i), a]))
        return results

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

    def table(self, plate, headers="firstrow", **kwargs):
        """
        return a tabulate object of plate.array
        
        :param plate: numpy.array of a plate object
        :param kwargs: keys arguments use by tabulate function
        :return:
        """
        return tabulate(plate, headers=headers, **kwargs)

    def iter_plate(self, plate, order="C"):
        """
        generator return [well, value]
        
        :param plate: numpy.array of plate object
        :param order: iterate by column C or by row R
        """
        columns = plate[0, 1:]
        rows = plate[1:, 0:1]
        values = plate[1:, 1:]
        if order == "C":
            order = "F"
        elif order == "R":
            order = "C"
        res = []
        for row, column, value in np.nditer([rows, columns, values], order=order):
            well, value = ''.join([str(row), str(column)]), str(value)
            yield [well, value]

    def iter_evaluate(self, plate, order="C", acumulate=True):
        """
        return a list [[well, value1, value2, value3],]
        
        :param plate:
        :param order:
        :param acumulate:
        :return:
        """
        dim = dimension(plate)
        if dim:
            value = list(map(lambda p: list(self.iter_plate(p, order=order)), [p for p in plate]))
        else:
            value = list(self.iter_plate(plate, order))
        if dim and acumulate:
            for a in range(1, len(value)):
                for i in range(len(value[0])):
                    if value[0][i][0] == value[a][i][0]:
                        value[0][i].append(value[a][i][1])
                    else:
                        pass
            value = value[0]
        return value

    def iterate(self, order="C", acumulate=True):
        """

        :param order:
        :param acumulate:
        :return:
        """
        yield from self.iter_evaluate(self.plate, order=order, acumulate=acumulate)

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
        dim = dimension(plate)
        if dim:
            results = {}
            n = 0
            for p in plate:
                results[n] = self.count(p)
                n += 1
        else:
        	results = self.count(plate)
        return results

    def counts(self):
        """

        :return:
        """
        return self.count_elements(self.plate)


if __name__ == '__main__':
    v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'], 'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
    Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}
    Plate = Plate(1, key="id")
    Plate.add_values(Value)
    print(Plate.table(Plate.plate, stralign="center", tablefmt="pipe"))
    print(Plate.plate.shape)
    print(Plate.plate_array)
    multi = np.array([Plate.plate, Plate.plate])
"""
    # print(multi)
    print(list(Plate.iterate(order="C")))
# print(Plate.table(Plate.counts(), headers="key"))
    f = open('table_html.html', 'w')
	#f.write(str(Plate.count_elements(multi)))
	#f.write(str(list(Plate.iter_evaluate(multi, acumulate=False))))
    f.write(Plate.table(Plate.plate, stralign="center", tablefmt="html"))
    f.close()

"""