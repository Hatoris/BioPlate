import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data
from BioPlate.utilitis import like_read_excel, as_read_excel, like_read_excel_stack, remove_tail, like_read_data, like_read_data_stack, like_read_count
from BioPlate.Plate import BioPlate
from BioPlate.writer.to_excel import BioPlateToExcel
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from string import ascii_uppercase
from tabulate import tabulate


class TestPlateToExcel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
        cls.pdb = PlateDB(db_name='test_plate.db')
        cls.pdb.add_plate(numWell=96,
              numColumns=12,
              numRows=8,
              surfWell=0.29,
              maxVolWell=200,
              workVolWell=200,
              refURL='https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf')

    @classmethod
    def tearDownClass(cls):
        """
        This function is run one time at the end of tests
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath(Path(__file__).parent.parent, 'BioPlate/database/DBFiles', 'test_plate.db')).unlink()
            Path(PurePath(Path(__file__).parent.parent, 'BioPlate/database/DBFiles', 'test_plate_historic.db')).unlink()

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.PTE = BioPlateToExcel("test.xlsx")
        v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
        v1 = {'A[2,8]': 'VC1', 'H[2,8]': 'MS1', '1-4[B,G]': ['MLR1', 'NT1', '1.3', '1.4'],
             'E-G[8,10]': ['Val4', 'Val5', 'Val6']}
        v2 = {'A[2,8]': 'Top', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
        v3 = {'A[2,8]': 'Bot', 'H[2,8]': 'MS1', '1-4[B,G]': ['MLR1', 'NT1', '1.3', '1.4'],
             'E-G[8,10]': ['Val4', 'Val5', 'Val6']}
        self.plt = BioPlate({"id" : 1}, db_name='test_plate.db')
        self.plt.set(v)
        self.plt1 = BioPlate(12, 8)
        self.plt1.set(v1)
        self.stack = self.plt + self.plt1
        self.Inserts = BioPlate(12, 8, inserts=True)
        self.Inserts.top.set(v)
        self.Inserts.bot.set(v3)
        self.Inserts1 = BioPlate(12, 8, inserts=True)
        self.Inserts1.bot.set(v1)
        self.Inserts1.top.set(v2)
        self.stacki = self.Inserts + self.Inserts1
        

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath("test.xlsx")).unlink()

###TEST REPRESENTATION SHEET
    def test_representation_BioPlate(self):
        read_excel = as_read_excel(self.PTE, "representation", self.plt, "test.xlsx", "plate_representation")
        rm_empty = like_read_excel(self.plt)
        self.assertEqual(read_excel, rm_empty)
  
    def test_representation_BioPlate_hd(self):
        c = {"header" : False}
        read_excel = as_read_excel(self.PTE, "representation", self.plt, "test.xlsx", "plate_representation", conditions= c)
        rm_empty = like_read_excel(self.plt, header=False)
        self.assertEqual(read_excel, rm_empty)
        
    def test_representation_BioPlateInserts(self):
        read_excel = as_read_excel(self.PTE, "representation", self.Inserts, "test.xlsx", "plate_representation")
        rm_empty = like_read_excel(self.Inserts)
        self.assertEqual(read_excel, rm_empty)        

    def test_representation_BioPlateInserts_hd(self):
        c = {"header" : False}
        read_excel = as_read_excel(self.PTE, "representation", self.Inserts, "test.xlsx", "plate_representation", conditions= c)
        rm_empty = like_read_excel(self.Inserts, header=False)
        self.assertEqual(read_excel, rm_empty)      
        
    def test_representation_BioPlateStack_bp(self):
        read_excel = as_read_excel(self.PTE, "representation", self.stack, "test.xlsx", "plate_representation")
        rm_empty = like_read_excel_stack(self.stack)
        self.assertEqual(read_excel, rm_empty)  

    def test_representation_BioPlateStack_bp_hd( self):
        c = {"header" : False}
        read_excel = as_read_excel(self.PTE, "representation", self.stack, "test.xlsx", "plate_representation", conditions=c)
        rm_empty = like_read_excel_stack(self.stack, header=False)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateStack_bpi(self):
        read_excel = as_read_excel(self.PTE, "representation", self.stacki, "test.xlsx", "plate_representation")
        rm_empty = like_read_excel_stack(self.stacki)
        self.assertEqual(read_excel, rm_empty)  

    def test_representation_BioPlateStack_bpi_hd( self):
        c = {"header" : False}
        read_excel = as_read_excel(self.PTE, "representation", self.stacki, "test.xlsx", "plate_representation", conditions=c)
        rm_empty = like_read_excel_stack(self.stacki, header=False)
        self.assertEqual(read_excel, rm_empty)
        
###TEST DATA SHEET        
    def  test_data_BioPlate(self):
        c = None
        read_excel = as_read_excel(self.PTE, "data", self.plt, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data(self.plt)
        self.assertEqual(read_excel, rm_empty) 

    def  test_data_BioPlate_row(self):
        c = {"order" : "R"}
        read_excel = as_read_excel(self.PTE, "data", self.plt, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data(self.plt, order="R")
        self.assertEqual(read_excel, rm_empty)
        
    def  test_data_BioPlateInserts(self):
        c = None
        read_excel = as_read_excel(self.PTE, "data", self.Inserts, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data(self.Inserts)
        self.assertEqual(read_excel, rm_empty) 

    def  test_data_BioPlateInserts_row(self):
        c = {"order" : "R"}
        read_excel = as_read_excel(self.PTE, "data", self.Inserts, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data(self.Inserts, order="R")
        self.assertEqual(read_excel, rm_empty)

    def  test_data_BioPlateInserts_row_acc(self):
        c = {"order" : "R", "accumulate" : False}
        read_excel = as_read_excel(self.PTE, "data", self.Inserts, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data(self.Inserts, order="R", accumulate= False)
        self.assertEqual(read_excel, rm_empty)  

    def  test_data_BioPlateStack_bp(self):
        c = None
        read_excel = as_read_excel(self.PTE, "data", self.stack, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data_stack(self.stack)
        self.assertEqual(read_excel, rm_empty) 

    def  test_data_BioPlateStack_bp_row(self):
        c = {"order" : "R"}
        read_excel = as_read_excel(self.PTE, "data", self.stack, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data_stack(self.stack, order="R")
        self.assertEqual(read_excel, rm_empty)
        
    def  test_data_BioPlateStack_bp_row_acc(self):
        c = {"order" : "R", "accumulate" : False}
        read_excel = as_read_excel(self.PTE, "data", self.stack, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data_stack(self.stack, order="R", accumulate=False)
        self.assertEqual(read_excel, rm_empty)          
        
    def  test_data_BioPlateStack_bpi(self):
        c = None
        read_excel = as_read_excel(self.PTE, "data", self.stacki, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data_stack(self.stacki)
        self.assertEqual(read_excel, rm_empty) 

    def  test_data_BioPlateStack_bpi_row(self):
        c = {"order" : "R"}
        read_excel = as_read_excel(self.PTE, "data", self.stacki, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data_stack(self.stacki, order="R")
        self.assertEqual(read_excel, rm_empty)
        
    def  test_data_BioPlateStack_bpi_row_acc( self):
        c = {"order" : "R", "accumulate" : False}
        read_excel = as_read_excel(self.PTE, "data", self.stacki, "test.xlsx", "plate_data", conditions=c)
        rm_empty = like_read_data_stack(self.stacki, order="R", accumulate=False)
        self.assertEqual(read_excel, rm_empty)                                         
###TEST COUNT SHEET                                                                                                           		
    def  test_count_BioPlate(self):
        c = None
        read_excel = as_read_excel(self.PTE, "count", self.plt, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.plt)
        self.assertEqual(read_excel, rm_empty)
        
    def  test_count_BioPlate_emp(self):
        c = {"empty" : "vide"}
        read_excel = as_read_excel(self.PTE, "count", self.plt, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.plt, empty="vide")
        self.assertEqual(read_excel, rm_empty)
        
    def  test_count_BioPlateInserts(self):
        c = None
        read_excel = as_read_excel(self.PTE, "count", self.Inserts, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.Inserts, Inserts=True)
        self.assertEqual(read_excel, rm_empty)
        
    def  test_count_BioPlateInserts(self):
        c = {"empty" : "vide"}
        read_excel = as_read_excel(self.PTE, "count", self.Inserts, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.Inserts, empty="vide", Inserts=True)
        self.assertEqual(read_excel, rm_empty)        
        
    def  test_count_BioPlateStack_bp(self):
        c = None
        read_excel = as_read_excel(self.PTE, "count", self.stack, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.stack)
        self.assertEqual(read_excel, rm_empty)
        
    def  test_count_BioPlateStack_bp_em(self):
        c = {"empty" : "vide"}
        read_excel = as_read_excel(self.PTE, "count", self.stack, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.stack, empty="vide")
        self.assertEqual(read_excel, rm_empty)

    def  test_count_BioPlateStack_bpi(self):
        c = None
        read_excel = as_read_excel(self.PTE, "count", self.stacki, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.stacki, Inserts=True)
        self.assertEqual(read_excel, rm_empty)
        
    def  test_count_BioPlateStack_bpi_em(self):
        c = {"empty" : "vide"}
        read_excel = as_read_excel(self.PTE, "count", self.stacki, "test.xlsx", "plate_count", conditions=c)
        rm_empty = like_read_count(self.stacki, empty="vide", Inserts=True)
        self.assertEqual(read_excel, rm_empty)

if __name__ == "__main__":
    unittest.main()
