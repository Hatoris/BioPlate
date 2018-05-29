import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate import BioPlate
from BioPlate.Stack import BioPlateStack
from string import ascii_uppercase
from tabulate import tabulate


class TestPlate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
        cls.plt = BioPlate(12, 8)
        cls.plt.set("A1", "test")
        cls.plt1 = BioPlate(12, 8)
        cls.plt1.set("A1", "test1")
        cls.stack = cls.plt + cls.plt1
        cls.plt2 = BioPlate(12, 8)
       
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

    def test__repr__(self):
         self.assertEqual(str(self.stack), str(np.array([self.plt, self.plt1])))
         
    def test__setitem__(self):
         self.stack[0, 1, 2] = "testset"
         self.assertEqual(self.stack[0][1,2], "testset")
         
     def test__add__(self):
         pass
         

if __name__ == "__main__":
    unittest.main()
 