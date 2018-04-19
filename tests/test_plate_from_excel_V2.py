import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data, save_data
from BioPlate.utilitis import like_read_excel, as_read_excel, like_read_excel_stack, remove_tail, like_read_data, like_read_data_stack, like_read_count, remove_np_tail
from BioPlate.Plate import BioPlate
from BioPlate.Inserts import BioPlateInserts
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
        
        self.PTE_BPI_header = BioPlateToExcel("bpi_header.xlsx", header=True)
        self.PTE_BPI_header.representation( self.Inserts)        
        self.PTE_BPI_header.close()
                   
        self.PTE_BPS_no_header = BioPlateToExcel("bps_header.xlsx", header=True)
        self.PTE_BPS_no_header.representation( self.stack)
        self.PTE_BPS_no_header.close()

        self.PTE_BPIS_header = BioPlateToExcel("bpis_header.xlsx", header=True)
        self.PTE_BPIS_header.representation( self.stacki)
        self.PTE_BPIS_header.close()
                        
        self.PTE_BPI_no_header = BioPlateToExcel("bpi_no_header.xlsx", header=False)
        self.PTE_BPI_no_header.representation( self.Inserts)        
        self.PTE_BPI_no_header.close()
        self.PTE_BP_header.representation(self.stack)
        #self.PTE_BPI_multisheet = BioPlateToExcel("bpi_multisheets")
        

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath("bp_header.xlsx")).unlink()
            Path(PurePath("bpi_header.xlsx")).unlink()
            Path(PurePath("bps_header.xlsx")).unlink()
            Path(PurePath("bpis_header.xlsx")).unlink()
            Path(PurePath("bpi_no_header.xlsx")).unlink()


    def test_get__no_empty_sheets(self):
        file = BioPlateFromExcel("bp_header.xlsx")
        read = file._get_no_empty_sheets()
        as_read = OrderedDict([("plate_representation", list(map(remove_tail, map(list, self.plt))))])
        self.assertEqual(read, as_read)

    def test_guess_type(self):
        bp = BioPlateFromExcel("bp_header.xlsx")
        tbp = bp._guess_type(bp.no_empty_sheets["plate_representation"])
        bpi = BioPlateFromExcel("bpi_header.xlsx")
        tbpi = bpi._guess_type(bpi.no_empty_sheets["plate_representation"])
        bps = BioPlateFromExcel("bps_header.xlsx")
        tbps = bps._guess_type(bps.no_empty_sheets["plate_representation"])
        bpis = BioPlateFromExcel("bpis_header.xlsx")
        tbpis = bpis._guess_type(bpis.no_empty_sheets["plate_representation"])
        self.assertEqual(tbp, (BioPlate, False))
        self.assertEqual(tbpi, (BioPlateInserts, False))
        self.assertEqual(tbps, (BioPlate, True))
        self.assertEqual(tbpis, (BioPlateInserts, True))

    def test_guess_column_row(self):
        bp = BioPlateFromExcel("bp_header.xlsx")
        tbp = bp._guess_column_row(bp.no_empty_sheets["plate_representation"])
        bpi = BioPlateFromExcel("bpi_header.xlsx")
        tbpi = bpi._guess_column_row(bpi.no_empty_sheets["plate_representation"])
        bps = BioPlateFromExcel("bps_header.xlsx")
        tbps = bps._guess_column_row(bps.no_empty_sheets["plate_representation"])
        bpis = BioPlateFromExcel("bpis_header.xlsx")
        tbpis = bpis._guess_column_row(bpis.no_empty_sheets["plate_representation"])
        self.assertEqual(tbp, (12, 8))
        self.assertEqual(tbpi, (12, 8))
        self.assertEqual(tbps, (12, 8))
        self.assertEqual(tbpis, (12, 8))

    def test_get_plate_informations(self):
        bp = BioPlateFromExcel("bp_header.xlsx")
        tbp = bp._get_plate_informations(bp.no_empty_sheets["plate_representation"])
        bpi = BioPlateFromExcel("bpi_header.xlsx")
        tbpi = bpi._get_plate_informations(bpi.no_empty_sheets["plate_representation"])
        bps = BioPlateFromExcel("bps_header.xlsx")
        tbps = bps._get_plate_informations(bps.no_empty_sheets["plate_representation"])
        bpis = BioPlateFromExcel("bpis_header.xlsx")
        tbpis = bpis._get_plate_informations(bpis.no_empty_sheets["plate_representation"])
        self.assertEqual(tbp, (BioPlate, False, 12, 8))
        self.assertEqual(tbpi, (BioPlateInserts, False, 12, 8))
        self.assertEqual(tbps, (BioPlate, True, 12, 8))
        self.assertEqual(tbpis, (BioPlateInserts, True, 12, 8))

    def test_get_BioPlate_object(self):
        bp = BioPlateFromExcel("bp_header.xlsx")
        tbp = bp._get_BioPlate_object()["plate_representation"]
        bpi = BioPlateFromExcel("bpi_header.xlsx")
        tbpi = bpi._get_BioPlate_object()["plate_representation"]
        bps = BioPlateFromExcel("bps_header.xlsx")
        tbps = bps._get_BioPlate_object()["plate_representation"]
#        bpis = BioPlateFromExcel("bpis_header.xlsx")
#        tbpis = bpis._get_BioPlate_object()["plate_representation"] 
        np.testing.assert_array_equal(tbp, self.plt)
        np.testing.assert_array_equal(tbpi, self.Inserts)
        #np.testing.assert_array_equal(tbps, self.stack)
        #self.assertEqual(tbpis, self.stacki)


if __name__ == "__main__":
    unittest.main()
