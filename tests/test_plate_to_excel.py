import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate.plate import Plate
from BioPlate.plate_to_excel import plateToExcel
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
        self.plt = Plate(96, db_name='test_plate.db')
        v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
        self.plt.add_values(v)
        PTE = plateToExcel("test.xlsx")

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath("test.xlsx")).unlink()

    def test_open_excel_file(self):
        pass

    def test_select_worksheet(self):
        pass

    def test_close(self):
        pass

    def test_past_values(self):
        pass


if __name__ == "__main__":
    unittest.main()
