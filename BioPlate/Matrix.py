import re
import numpy as np
import BioPlate.utilitis as bpu
import types
import time 



class BioPlateMatrix:
    """
    format of well :
        - B5
        - 6A
        - C[2,8]
        - 4[C,G]
        - 1-8[A,C]
        - A-G[1,8]
    """
   
    _WELL_CACHE = {}
    
    def __new__(cls, well):
        well = well.replace(" ", "")
        BioPlateMatrix._test_for_0(well)
        if well not in BioPlateMatrix._WELL_CACHE:
            result = BioPlateMatrix._index_from_well(well)
            BioPlateMatrix._WELL_CACHE[well] = result
        return BioPlateMatrix._WELL_CACHE[well]
    
    @staticmethod
    def _index_from_well(well):
         row, column = BioPlateMatrix._base_row_column(well)
         index = BioPlateMatrix._index_row_column(row, column)
         #comment to return generator
         if isinstance(index, types.GeneratorType):
             index = list(index)
         return index

    @staticmethod
    def _base_row_column(well):
        """
        split string well to row column
        """
        try: #A5, 2[B-H]
            row, column =  list(reversed(sorted(filter(None, re.split('(\d+)', well)))))
        except ValueError:
            try: #D[1-6]
                row, column =  list(sorted(filter(None, re.split('([A-Z])', well))))
            except ValueError: #1-5[D-F]
                comp = re.compile('(\w+[\-|\,]\w+)')
                row, column = re.findall(comp, well) 
        return row, column
     
    @staticmethod
    def _multi_row_column(multi):
        """
        From multi value return only row or column
        """
        comp = re.compile("(\w+)")
        multi1, multi2 =  list(sorted(filter(comp.search, re.split('(\W)', multi))))
        return multi1, multi2
                    
     
    @staticmethod
    def _index_row_column(row, column):
        """
        get split of row or  column in multi value
        """
        comp = re.compile('(\w+)')
        lrow = len(row)
        lcolumn = len(re.findall(comp, column))
        if lrow > 1 and lcolumn > 1:
            return BioPlateMatrix.__m_row_m_column( row, column)
        elif lrow == 1 and lcolumn == 1:
            row = BioPlateMatrix._well_letter_index(row)
            return int(row), int(column)
        elif lrow > 1 and lcolumn == 1:
            row1, row2 = list(map( BioPlateMatrix._well_letter_index, BioPlateMatrix._multi_row_column(row)))
            return "R", int(row1), int(row2) + 1, int(column)
        elif lcolumn > 1 and lrow == 1:
           column1, column2 = sorted(map(int, BioPlateMatrix._multi_row_column(column)))
           row = BioPlateMatrix._well_letter_index(row)
           return "C", int(row), column1, column2 + 1
                      
    @staticmethod 
    def __m_row_m_column(row, column):
        val = re.compile('(\w+)')
        comp = lambda x : list(BioPlateMatrix._multi_row_column(x))
        iterator, selector = list(map(comp, [row, column]))
        try:
            row1, row2 = list(map( BioPlateMatrix._well_letter_index, selector))
            iterator = sorted(map(int, iterator))
            for column in range(iterator[0], iterator[1] + 1):
                yield "R", int(row1), int(row2), column
        except ValueError:
                row1, row2 = list(map( BioPlateMatrix._well_letter_index, iterator))
                column1, column2 = sorted(map(int, [selector[0], selector[1]]))
                for row in range(row1, row2 + 1):
                    yield "C", int(row), column1, column2 + 1

    @staticmethod
    def _well_letter_index(row_letter):
        """
        get index for a given letter (eg : C)
        
        :param row_letter: C => letter of a row
        :return: 3 => index of row C in plate.array
        """
        return np.searchsorted(bpu._LETTER, row_letter) + 1
       
    @staticmethod 
    def _test_for_0(well):
        zero = re.compile('(^\D*0\D*$)')
        test = list(filter(zero.search, re.split("(\d+)", well)))
        if not test:
            pass
        else:
             raise ValueError(f"well = {well} is not allowed, column 0 is forbiden")
       

if __name__ == "__main__":
    #row, column = BioPlateMatrix._base_row_column("A8")
    #print(row, column)
    t0 = time.time()
    for well in ["A8", "G7", "8E", "5D", "2[A-C]", "G[2-8]", "3-11[A-D]", "F-J[2-18]", "10-8[A-E]"]:
        #BioPlateMatrix._test_for_0(well)
        row, column, *trash = BioPlateMatrix(well)
        print(well, BioPlateMatrix(well))
    t1 = time.time()
    for well in ["A8", "G7", "8E", "5D", "2[A-C]", "G[2-8]", "1-3[A-D]", "F-J[2-8]"]:
        print(well, BioPlateMatrix(well))
    t2 = time.time()
    print("r1", t1 - t0, "r2", t2 - t1)
    
    
        
        #print(BioPlateMatrix._index_from_well( well))
        #print(well)
       #row, column = BioPlateMatrix._base_row_column(well)
       #print(row, column)
       #a, b, *c = BioPlateMatrix._index_row_column(row, column)
       #print(well, a, b, *c)
   #for well in ["1-3[A-D]", "F-J[2-8]"]:
        
    """
       row, column =  BioPlateMatrix._base_row_column(well)
       print(well, row, column)
       print(well, len(row), len(column))
       if len(row) > 1:
           comp = re.compile("\w")
           row1, row2 =  list(sorted(filter(comp.search, re.split('(\W)', row))))
           print(well, row1, row2, column)
       elif len(column) > 1:
           comp = re.compile("\w")
           column1, column2 =  list(sorted(filter(comp.search, re.split('(\W)', column))))
           print(well, row, column1, column2)
  """