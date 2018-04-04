import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate.utilitis import remove_empty_iterate, dict_unique
from BioPlate.Manipulation import BioPlateManipulation



class TestBioPlateManipulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
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
        self.BPM = BioPlateManipulation()
        
    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass
        
    def test_matrix_well(self):
        self.assertEqual( self.BPM.matrix_well("A1"), (1, 1))
        self.assertEqual( self.BPM.matrix_well("E12"), (5, 12))
        
        
        
        
        
        
if __name__ == "__main__":
     unittest.main()
       