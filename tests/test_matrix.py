import unittest
import contextlib
import numpy as np
import BioPlate.utilitis as bpu

from pathlib import Path, PurePath
from BioPlate.Plate import BioPlate
from BioPlate.Matrix import BioPlateMatrix
from string import ascii_uppercase




class TestMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
        #cls.plt = BioPlate(12, 8)        
#        Value = {'A1': 'A1', 'A2': 'A2', 'A3': 'A3', 'A4': 'A4', 'A5': 'A5', 'A6': 'A6', 'A7': 'A7', 'A8': 'A8', 'A9': 'A9', 'A10': 'A10', 'A11': 'A11', 'A12': 'A12', 'B1': 'B1', 'B2': 'B2', 'B3': 'B3', 'B4': 'B4', 'B5': 'B5', 'B6': 'B6', 'B7': 'B7', 'B8': 'B8', 'B9': 'B9', 'B10': 'B10', 'B11': 'B11', 'B12': 'B12', 'C1': 'C1', 'C2': 'C2', 'C3': 'C3', 'C4': 'C4', 'C5': 'C5', 'C6': 'C6', 'C7': 'C7', 'C8': 'C8', 'C9': 'C9', 'C10': 'C10', 'C11': 'C11', 'C12': 'C12', 'D1': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4', 'D5': 'D5', 'D6': 'D6', 'D7': 'D7', 'D8': 'D8', 'D9': 'D9', 'D10': 'D10', 'D11': 'D11', 'D12': 'D12', 'E1': 'E1', 'E2': 'E2', 'E3': 'E3', 'E4': 'E4', 'E5': 'E5', 'E6': 'E6', 'E7': 'E7', 'E8': 'E8', 'E9': 'E9', 'E10': 'E10', 'E11': 'E11', 'E12': 'E12', 'F1': 'F1', 'F2': 'F2', 'F3': 'F3', 'F4': 'F4', 'F5': 'F5', 'F6': 'F6', 'F7': 'F7', 'F8': 'F8', 'F9': 'F9', 'F10': 'F10', 'F11': 'F11', 'F12': 'F12', 'G1': 'G1', 'G2': 'G2', 'G3': 'G3', 'G4': 'G4', 'G5': 'G5', 'G6': 'G6', 'G7': 'G7', 'G8': 'G8', 'G9': 'G9', 'G10': 'G10', 'G11': 'G11', 'G12': 'G12', 'H1': 'H1', 'H2': 'H2', 'H3': 'H3', 'H4': 'H4', 'H5': 'H5', 'H6': 'H6', 'H7': 'H7', 'H8': 'H8', 'H9': 'H9', 'H10': 'H10', 'H11': 'H11', 'H12': 'H12'}
#        cls.plt.set(Value)
        pass
       

    @classmethod
    def tearDownClass(cls):
        """
        This function is run one time at the end of tests
        :return:
        """
        pass

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        pass
        

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass
        
    def test_general(self):
        self.assertEqual(BioPlateMatrix("A2"), bpu.EL("W", 1, 2))
        self.assertEqual(BioPlateMatrix("5G"), bpu.EL("W", 7, 5))
        
        self.assertEqual(BioPlateMatrix("B[2,8]"), bpu.EL('R', 2, slice(2, 9, 1)))
        self.assertEqual(BioPlateMatrix("2[B-G]"), bpu.EL('C', slice(2, 8, 1), 2))
        
        self.assertEqual(BioPlateMatrix("A-G[1-8]"), bpu.EL("R", slice(1, 8, 1), slice(1, 9,1)))
        self.assertEqual(BioPlateMatrix("1-8[A-G]"), bpu.EL("C", slice(1, 8, 1), slice(1, 9,1)))
        
        self.assertEqual(BioPlateMatrix('C'), bpu.EL("R", slice(4), slice(1, None)))
        self.assertEqual(BioPlateMatrix('12'), bpu.EL("C", slice(1, None), slice(13)))
  
    def test_base_row_column(self):
         self.assertEqual(BioPlateMatrix._base_row_column("A1"), ('1', 'A'))
         self.assertEqual(BioPlateMatrix._base_row_column("A[2,5]"), ('[2,5]', 'A'))
         self.assertEqual(BioPlateMatrix._base_row_column("1[A-C]"), ('1', '[A-C]'))
         self.assertEqual(BioPlateMatrix._base_row_column("A-B[1-6]"), ('1-6', 'A-B'))
                    
    def test_multi_row_column(self):
        self.assertEqual(BioPlateMatrix._multi_row_column("A-B"), ('A', 'B'))
        self.assertEqual(BioPlateMatrix._multi_row_column("C,G"), ('C', 'G'))
        self.assertEqual(BioPlateMatrix._multi_row_column("U,D"), ('D','U'))
        
    def test_index_row_column(self):
        self.assertEqual(BioPlateMatrix._index_row_column('A', '1'),  bpu.EL("W", 1, 1))
        self.assertEqual(BioPlateMatrix._index_row_column('D', '10'), bpu.EL("W", 4, 10))
        self.assertEqual(BioPlateMatrix._index_row_column('D-G', '10'), bpu.EL('C', slice(4,  8, 1), 10))
        self.assertEqual(BioPlateMatrix._index_row_column('G-I', '5-8'), bpu.EL("R", slice(7, 10, 1), slice(5,9,1)))
        self.assertEqual(BioPlateMatrix._index_row_column('G', '5-8'), bpu.EL('R', 7,  slice(5, 9, 1)))
        self.assertEqual(BioPlateMatrix._index_row_column('B-E', '5'), bpu.EL('C', slice(2,  6, 1), 5))
        
    def test_well_letter_index(self):
        self.assertEqual(BioPlateMatrix._well_letter_index('A'), 1)
        self.assertEqual(BioPlateMatrix._well_letter_index('G'), 7)           
        
    def test_all_row_column(self):
        self.assertEqual(BioPlateMatrix._all_row_column('A'), bpu.EL("R", slice(2), slice(1, None)))
        self.assertEqual(BioPlateMatrix._all_row_column(3), bpu.EL("C", slice(1, None), slice(4)))
       
        
    def test__test_row_or_column(self):
        self.assertTrue(BioPlateMatrix._test_row_or_column('A'))
        self.assertTrue(BioPlateMatrix._test_row_or_column('12'))
        self.assertTrue(BioPlateMatrix._test_row_or_column(10))
        

if __name__ == "__main__":
    unittest.main()
