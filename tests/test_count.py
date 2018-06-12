import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate.plate import BioPlate
from BioPlate.count import BioPlateCount


class TestPlate(unittest.TestCase):
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
        self.plt = BioPlate(12, 8)
        self.plt1 = BioPlate(12, 8)
        self.stack = self.plt + self.plt1
        self.Inserts = BioPlate(12, 8, inserts=True)
        self.Inserts1 = BioPlate(12, 8, inserts=True)
        self.stacki = self.Inserts + self.Inserts1
        self.Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}
        self.Value2 = {"A1": "Control1", "D[2,9]": "Test3", "12[B,H]": "Test4"}

        def test_reverse(self):
            pass

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test_count_BioPlate(self):
        self.assertDictEqual(
            BioPlateCount(self.plt.set(self.Value)),
            {"": 80, "Control": 1, "Test1": 9, "Test2": 6},
        )
        self.assertDictEqual(
            BioPlateCount(self.plt.set(self.Value), reverse=True),
            {"": 80, "Control": 1, "Test2": 6, "Test1": 9},
        )

    def test_count_BioPlateInserts(self):
        self.Inserts.top.set(self.Value)
        self.Inserts.bot.set(self.Value2)
        self.assertDictEqual(
            BioPlateCount(self.Inserts),
            {
                "top": {"Control": 1, "Test1": 9, "Test2": 6, "": 80},
                "bot": {"Control1": 1, "Test3": 8, "Test4": 7, "": 80},
            },
        )

    def test_count_BioPlateStack_BioPlate(self):
        self.plt.set(self.Value)
        self.plt1.set(self.Value2)
        self.assertDictEqual(
            BioPlateCount(self.stack),
            {
                0: {"Control": 1, "Test1": 9, "Test2": 6, "": 80},
                1: {"Control1": 1, "Test3": 8, "Test4": 7, "": 80},
            },
        )

    def test_count_BioPlateStack_BioPlateInserts(self):
        self.Inserts.top.set(self.Value)
        self.Inserts.bot.set(self.Value2)
        self.Inserts1.top.set(self.Value)
        self.Inserts1.bot.set(self.Value2)
        self.assertEqual(
            BioPlateCount(self.stacki),
            {
                0: {
                    "top": {"Control": 1, "Test2": 6, "Test1": 9, "": 80},
                    "bot": {"Control1": 1, "Test3": 8, "Test4": 7, "": 80},
                },
                1: {
                    "top": {"Control": 1, "Test1": 9, "Test2": 6, "": 80},
                    "bot": {"Control1": 1, "Test3": 8, "Test4": 7, "": 80},
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
