import unittest
import contextlib
import numpy as np
import BioPlate.utilitis as bpu

from pathlib import Path, PurePath
from BioPlate import BioPlate
from BioPlate.matrix import *
from string import ascii_uppercase

class TestMatrix(unittest.TestCase):
    
    def test_general(self):
        self.assertEqual(BioPlateMatrix("A2"), bpu.EL("W", 1, 2))
        self.assertEqual(BioPlateMatrix("5G"), bpu.EL("W", 7, 5))
        self.assertEqual(BioPlateMatrix("2-10[A]"), bpu.EL("C", 1, slice(2, 11, 1)))
        self.assertEqual(BioPlateMatrix("B[2,8]"), bpu.EL("R", 2, slice(2, 9, 1)))
        self.assertEqual(BioPlateMatrix("2[B-G]"), bpu.EL("C", slice(2, 8, 1), 2))
        self.assertEqual(
            BioPlateMatrix("A-G[1-8]"), bpu.EL("R", slice(1, 8, 1), slice(1, 9, 1))
        )
        self.assertEqual(
            BioPlateMatrix("1-8[A-G]"), bpu.EL("C", slice(1, 8, 1), slice(1, 9, 1))
        )
        
    def test_split_well_infos(self):
        self.assertEqual(split_well_infos("12"), ("12", None))
        self.assertEqual(split_well_infos("12[A-B]"), ("12", "A-B"))
        self.assertEqual(split_well_infos("A1"), ("A", "1"))
        self.assertEqual(split_well_infos("A[2,5]"), ("A", "2,5"))
        self.assertEqual(split_well_infos("1[A-C]"), ("1", "A-C"))
        self.assertEqual(split_well_infos("A-B[1-6]"), ("A-B", "1-6"))
        self.assertEqual(split_well_infos("1-8[B-G]"), ("1-8", "B-G"))

    def test_split_multi_value(self):
        self.assertEqual(split_multi_value("A-C"), (1, 4))
        self.assertEqual(split_multi_value("2-10"), (2, 11))
        self.assertEqual(split_multi_value("A-B"), (1, 3))
        self.assertEqual(split_multi_value("C,G"), (3, 8))
        self.assertEqual(split_multi_value("U,D"), (4, 22))
        self.assertEqual(split_multi_value("12-1"), (1, 13))
    
    def test_row_index(self):
        self.assertEqual(row_index("A-C"), slice(1, 4, 1))
        self.assertEqual(row_index("C"), 3)

    def test_column_index(self):
        self.assertEqual(column_index("2-10"), slice(2, 11, 1))
        self.assertEqual(column_index("3"), 3)
                        
    def test_convert_letter_to_index(self):
        self.assertEqual(convert_letter_to_index("A"), 1)
        self.assertEqual( convert_letter_to_index("G"), 7)
        
    def test_one_well(self):
        self.assertEqual(one_well("A", "2", "R"), (1, 2, "W"))
        
    def test_is_zero(self):
        with self.assertRaises(ValueError) :
            is_zero("D[0-9]")
        with self.assertRaises(ValueError):
            is_zero("0")
        with self.assertRaises(ValueError) :
            is_zero("0-10[A-B]")
        self.assertEqual(is_zero("10"), None)

if __name__ == "__main__":
    unittest.main()   