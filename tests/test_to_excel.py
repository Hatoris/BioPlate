import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data
from BioPlate.utilitis import remove_empty_iterate, dict_unique
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
        self.PTE = plateToExcel("test.xlsx")
        self.plate_2_plates = np.array([self.plt.plate, self.plt.plate])
        self.plate_2_plates_no_hd = np.array([self.plt.plate[1:,1:], self.plt.plate[1:,1:]])

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath("test.xlsx")).unlink()

    def test_past_values(self):
    	rm_empty = remove_empty_iterate(list(self.plt.iterate()), hd=  [['well', 'value']])
    	self.PTE.past_values(list(self.plt.iterate()))
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_data']
    	self.assertEqual(read_excel, rm_empty)
    	
    def test_past_values_multi_plate_accumulate(self):
    	stack_acc = self.plt.iter_evaluate(self.plate_2_plates)
    	stack_acc_clean = remove_empty_iterate(stack_acc, hd=  [['well', 'value', 'value1']])
    	self.PTE.past_values(stack_acc)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_data']
    	self.assertEqual(read_excel, stack_acc_clean)
    	
    def test_past_values_multi_plate(self):
    	stack = self.plt.iter_evaluate(self.plate_2_plates, acumulate=False)
    	stack_clean = remove_empty_iterate(stack, hd=  [['well', 'value']])
    	self.PTE.past_values(stack)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_data']
    	self.assertEqual(read_excel, stack_clean)
    	
    def test_plate_representation(self):
    	self.PTE.plate_representation(self.plt.plate)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean = remove_empty_iterate(self.plt.plate.tolist())
    	clean[1].insert(1, '')
    	clean[8].insert(1, '')
    	for  row in [5,6, 7]:
    		for n in [5, 6, 7]:
    			clean[row].insert(n, '')
    	self.assertEqual(read_excel, clean)
    	
    def test_plate_information(self):
    	self.PTE.plate_information(self.plt.counts())
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean = [['', 'infos', 'count'], ]
    	for key, value in self.plt.counts().items():
    		test = ['', key, value]
    		clean.append(test)
    	self.assertEqual(read_excel, clean)
    	
    def test_plate_representation_no_header(self):
    	self.PTE.plate_representation(self.plt.plate, header=False)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean = remove_empty_iterate(self.plt.plate[1:,1:].tolist())
    	clean[0].insert(0, '')
    	clean[7].insert(0, '')
    	for  row in [4,5,6]:
    		for n in [4,5,6]:
    			clean[row].insert(n, '')
    	self.assertEqual(read_excel, clean)
    
    def test_plate_representation_multi_plate(self):
    	self.PTE.plate_representation(self.plate_2_plates)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean1 = remove_empty_iterate(self.plt.plate.tolist())
    	clean1[1].insert(1, '')
    	clean1[8].insert(1, '')
    	for  row in [5,6, 7]:
    		for n in [5, 6, 7]:
    			clean1[row].insert(n, '')
    	clean = clean1[:]
    	clean1.append([])
    	clean1 = clean1 + clean
    	self.assertEqual(read_excel, clean1)
    	
    def test_plate_information_multi(self):
    	cc = self.plt.count_elements(self.plate_2_plates)
    	self.PTE.plate_information(cc)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean = [['', 'plate', 'infos', 'count'], ]
    	for k, val in cc.items():
    		for key, value in val.items():
    			test = ['', k, key, value]
    			clean.append(test)
    	self.assertEqual(read_excel, clean)
    	
    def test_plate_information_multi_acumulate(self):
    	cc = self.plt.count_elements(self.plate_2_plates)
    	self.PTE.plate_information(cc, acumulate=True)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean = [['', 'infos', 'count'], ]
    	proper = dict_unique(cc)
    	for key, value in proper.items():
    		test = ['', key, value]
    		clean.append(test)
    	self.assertEqual(read_excel, clean)
    	
    def test_plate_representation_multi_plate_no_header(self):
    	self.PTE.plate_representation(self.plate_2_plates, header=False)
    	self.PTE.close()
    	read_excel = get_data("test.xlsx")['plate_representation']
    	clean1 = remove_empty_iterate(self.plt.plate[1:,1:].tolist())
    	clean1[0].insert(0, '')
    	clean1[7].insert(0, '')
    	for  row in [4,5,6]:
    		for n in [4,5,6]:
    			clean1[row].insert(n, '')
    	clean = clean1[:]
    	clean1.append([])
    	clean1 = clean1 + clean
    	self.assertEqual(read_excel, clean1)		

if __name__ == "__main__":
    unittest.main()
