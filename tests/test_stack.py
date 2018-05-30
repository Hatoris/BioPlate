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
        cls.plt2 = BioPlate(12, 8)
        cls.plt2.set("A1", "plt2")
        cls.plt3 = BioPlate(12,8)
        cls.plt3.set("A1", "plt3")
        cls.Ins = BioPlate(12, 8, inserts=True)
        cls.Ins.top.set("A1", "topIns")
        cls.Ins1 = BioPlate(12, 8, inserts=True)
        cls.Ins1.top.set("A1", "topIns1")
       
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
        self.stack = self.plt + self.plt1

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test__repr__(self):
         self.maxDiff = None
         self.assertEqual(str(self.stack), str(np.array([self.plt, self.plt1])))
         
    def test__setitem__(self):
         self.stack[0, 1, 2] = "testset"
         self.assertEqual(self.stack[0][1,2], "testset")
         
    def test__add__(self):
         Nstack = self.stack + self.plt2
         self.assertEqual(Nstack.name, "BioPlateStack")
         np.testing.assert_array_equal(Nstack[2], self.plt2)
         with self.assertRaises(ValueError):
             Nstack + self.plt2
         N2stack = self.plt2 + self.plt3
         Astack = self.stack + N2stack
         np.testing.assert_array_equal(Nstack[2], self.plt2)

    def test_change_args(self):
        Nstacki = self.Ins + self.Ins1
        self.assertEqual(Nstacki.get(0, "top", "A1"), "topIns")
        



if __name__ == "__main__":
    unittest.main()
 