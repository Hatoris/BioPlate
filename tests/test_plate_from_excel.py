import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data, save_data
from BioPlate.utilitis import like_read_excel, as_read_excel, like_read_excel_stack, remove_tail, like_read_data, like_read_data_stack, like_read_count
from BioPlate.Plate import BioPlate
from BioPlate.Stack import BioPlateStack
from BioPlate.writer.to_excel import BioPlateToExcel
from BioPlate.writer.from_excel_V2 import BioPlateFromExcel
from collections import OrderedDict

class TestPlateFromExcel(unittest.TestCase):
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
        v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
        v1 = {'A[2,8]': 'VC1', 'H[2,8]': 'MS1', '1-4[B,G]': ['MLR1', 'NT1', '1.3', '1.4'],
             'E-G[8,10]': ['Val4', 'Val5', 'Val6']}
        v2 = {'A[2,8]': 'Top', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
        v3 = {'A[2,8]': 'Bot', 'H[2,8]': 'MS1', '1-4[B,G]': ['MLR1', 'NT1', '1.3', '1.4'],
             'E-G[8,10]': ['Val4', 'Val5', 'Val6']}
        self.plt = BioPlate(12, 8)
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
        self.PTE_BP_header = BioPlateToExcel("bp_header.xlsx")
        self.PTE_BP_header.representation(self.plt)
        self.PTE_BP_header.close()
        self.PTE_BPI_no_header = BioPlateToExcel("bpi_no_header.xlsx", header=False)
        self.PTE_BPI_no_header.representation(self.Inserts)
        self.PTE_BPI_no_header.close()
        self.PTE_BPS_no_header = BioPlateToExcel("bps_no_header.xlsx", header=False)
        self.PTE_BPS_no_header.representation( self.stack)
        self.PTE_BPS_no_header.close()
        self.PTE_BP_header.representation(self.stack)
        #self.PTE_BPI_multisheet = BioPlateToExcel("bpi_multisheets")
        

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath("bp_header.xlsx")).unlink()
            Path(PurePath("bps_no_header.xlsx")).unlink()
            Path(PurePath("bpi_no_header.xlsx")).unlink()


    def test_get__no_empty_sheets(self):
        file = BioPlateFromExcel("bp_header.xlsx")
        read = file._get_no_empty_sheets()
        as_read = OrderedDict([("plate_representation", list(map(remove_tail, map(list, self.plt))))])
        self.assertEqual(read, as_read)

#    def test_BP_hd(self):
#        read = BioPlateFromExcel("bp_header.xlsx").BioPlate_representation["plate_representation"][0]
#        np.testing.assert_array_equal(self.plt, read)

#    def test_BPI_no_hd(self):
#        read = BioPlateFromExcel("bpi_no_header.xlsx",  plate_infos={"sheet_name" : "plate_representation",  "row" : 8, "column" : 12}, header=False, Inserts= True ).BioPlate_representation["plate_representation"][0]
#        print(read)
#        #print(self.Inserts[np.where(read != self.Inserts)])
#        #self.assertEqual(self.Inserts.all(), read.all())
#        np.testing.assert_equal(self.Inserts, read)


if __name__ == "__main__":
    unittest.main()
