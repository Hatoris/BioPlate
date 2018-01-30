import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate.plate import Plate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from string import ascii_uppercase
from tabulate import tabulate


class TestPlate(unittest.TestCase):

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

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test_Plate_init(self):
        self.assertEqual(str(self.plt.plates), "<plate N°1 : 96-12-8>")
        self.assertEqual(str(self.plt.letter), str(np.array(list(ascii_uppercase))))
        np.testing.assert_array_equal(self.plt.plate, np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                                ['A', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['B', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['C', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['F', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                                ['H', '', '', '', '', '', '', '', '', '', '', '', '']], dtype='U40'))

    def test_plate_array(self):
        np.testing.assert_array_equal(self.plt.plate, self.plt.plate_array)

    def test_matrix_well(self):
        self.assertEqual(self.plt.matrix_well('A2'), (1,2))
        self.assertEqual(self.plt.matrix_well('G7'), (7, 7))

    def test_add_value(self):
        np.testing.assert_array_equal(self.plt.add_value("B2", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value("A2", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value("H6", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value("12C", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value("E8", "Test"), np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                          ['A', '', 'Test', '', '', '', '', '', '', '', '', '', ''],
                                                          ['B', '', 'Test', '', '', '', '', '', '', '', '', '', ''],
                                                          ['C', '', '', '', '', '', '', '', '', '', '', '', 'Test'],
                                                          ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                          ['E', '', '', '', '', '', '', '', 'Test', '', '', '', ''],
                                                          ['F', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                          ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                          ['H', '', '', '', '', '', 'Test', '', '', '', '', '', '']], dtype='U40'))

    def test_add_value_row(self):
        np.testing.assert_array_equal(self.plt.add_value_row("C[3,12]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value_row("A[4,3]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value_row("F[9,12]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value_row("D[6,8]", 18),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', '', 'Test', 'Test', '', '', '', '', '', '', '', ''],
                                                ['B', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['C', '', '', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test'],
                                                ['D', '', '', '', '', '', '18', '18', '18', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', '', '', '', '', '', '', '', '', 'Test', 'Test', 'Test', 'Test'],
                                                ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', '', '', '', '', '', '', '']],
                                               dtype='U40'))
        np.testing.assert_array_equal(self.plt.add_value_row("D[1-7]", "Test"), self.plt.plate)
        self.assertEqual(self.plt.add_value_row("D[0,8]", 18), "can't assign value on 0")

    def test_add_value_column(self):
        np.testing.assert_array_equal(self.plt.add_value_column("3[C,E]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value_column("7[A,H]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value_column("12[F,A]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_value_column("1[C,F]", "Test"),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', '', '', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['B', '', '', '', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['C', 'Test', '', 'Test', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['D', 'Test', '', 'Test', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['E', 'Test', '', 'Test', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['F', 'Test', '', '', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['G', '', '', '', '', '', '', 'Test', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', '', 'Test', '', '', '', '', '']], dtype='U40'))

    def test_add_values(self):
        np.testing.assert_array_equal(self.plt.add_values({"A1" : "Test", "B3" : "Test"}), self.plt.plate)
        self.assertEqual(self.plt.add_values(["G1", "Test", "H3", "Test"]),
                         "<class 'list'> is a wrong format, dictionary should be used")

    def test_split_multi_row_column(self):
        self.assertEqual(self.plt.split_multi_row_column('A-E[1,5]'),
                         ['A[1,5]', 'B[1,5]', 'C[1,5]', 'D[1,5]', 'E[1,5]'])
        self.assertEqual(self.plt.split_multi_row_column('1-5[A,E]'),
                         ['1[A,E]', '2[A,E]', '3[A,E]', '4[A,E]', '5[A,E]'])
        self.assertEqual(self.plt.split_multi_row_column('E-A[1,5]'),
                         ['A[1,5]', 'B[1,5]', 'C[1,5]', 'D[1,5]', 'E[1,5]'])
        with self.assertRaises(SyntaxError):
            self.plt.split_multi_row_column('E:A[1,5]')

    def test_add_multi_value(self):
        with self.assertRaises(ValueError):
            self.plt.add_multi_value('A-C[1-5]', ["Test1", "Test2"])
        np.testing.assert_array_equal(self.plt.add_multi_value('A-C[1-5]', ["Test1", "Test2", "Test3"]), self.plt.plate)
        np.testing.assert_array_equal(self.plt.add_multi_value('F-H[1-3]', ["Test1", "Test2", "Test3"]),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1', '', '', '', '', '', '', ''],
                                                ['B', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2', '', '', '', '', '', '', ''],
                                                ['C', 'Test3', 'Test3', 'Test3', 'Test3', 'Test3', '', '', '', '', '', '', ''],
                                                ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', 'Test1', 'Test1', 'Test1', '', '', '', '', '', '', '', '', ''],
                                                ['G', 'Test2', 'Test2', 'Test2', '', '', '', '', '', '', '', '', ''],
                                                ['H', 'Test3', 'Test3', 'Test3', '', '', '', '', '', '', '', '', '']], dtype='U40'))

    def test_evaluate(self):
        with self.assertRaises(SyntaxError):
            self.plt.evaluate('A:C[1-5]', ["Test1", "Test2", "Test3"])
        np.testing.assert_array_equal(self.plt.evaluate("2[B,E]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.evaluate("A[1,5]", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.evaluate("1C", "Test"), self.plt.plate)
        np.testing.assert_array_equal(self.plt.evaluate("1-3[A,C]", ["Test1", "Test2", "Test3"]), self.plt.plate)
        np.testing.assert_array_equal(self.plt.evaluate("F-H[1,3]", ["Test1", "Test2", "Test3"]),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', 'Test1', 'Test2', 'Test3', 'Test', 'Test', '', '', '', '', '', '', ''],
                                                ['B', 'Test1', 'Test2', 'Test3', '', '', '', '', '', '', '', '', ''],
                                                ['C', 'Test1', 'Test2', 'Test3', '', '', '', '', '', '', '', '', ''],
                                                ['D', '', 'Test', '', '', '', '', '', '', '', '', '', ''],
                                                ['E', '', 'Test', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', 'Test1', 'Test1', 'Test1', '', '', '', '', '', '', '', '', ''],
                                                ['G', 'Test2', 'Test2', 'Test2', '', '', '', '', '', '', '', '', ''],
                                                ['H', 'Test3', 'Test3', 'Test3', '', '', '', '', '', '', '', '', '']], dtype='U40'))

    def test_well_letter_index(self):
        self.assertEqual(self.plt.well_letter_index("D"), 4)
        self.assertEqual(self.plt.well_letter_index("H"), 8)

    def test_letter_index(self):
        self.assertEqual(self.plt.letter_index("D"), 3)
        self.assertEqual(self.plt.letter_index("H"), 7)

    def test_index_letter(self):
        self.assertEqual(self.plt.index_letter(3), "D")
        self.assertEqual(self.plt.index_letter(7), "H")

    def test_all_in_one(self):
        v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
        result = np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                           ['A', '', 'VC', 'VC', 'VC', 'VC', 'VC', 'VC', 'VC', '', '', '', ''],
                           ['B', 'MLR', 'NT', '1.1', '1.2', '', '', '', '', '', '', '', ''],
                           ['C', 'MLR', 'NT', '1.1', '1.2', '', '', '', '', '', '', '', ''],
                           ['D', 'MLR', 'NT', '1.1', '1.2', '', '', '', '', '', '', '', ''],
                           ['E', 'MLR', 'NT', '1.1', '1.2', '', '', '', 'Val1', 'Val1', 'Val1', '', ''],
                           ['F', 'MLR', 'NT', '1.1', '1.2', '', '', '', 'Val2', 'Val2', 'Val2', '', ''],
                           ['G', 'MLR', 'NT', '1.1', '1.2', '', '', '', 'Val3', 'Val3', 'Val3', '', ''],
                           ['H', '', 'MS', 'MS', 'MS', 'MS', 'MS', 'MS', 'MS', '', '', '', '']], dtype='U40')
        np.testing.assert_array_equal(self.plt.add_values(v), result)
        self.assertEqual(self.plt.table(self.plt.plate), tabulate(result, headers='firstrow'))
    
    def test_save(self):
        	self.plt.add_value('H4', 'Test')
        	self.assertEqual(self.plt.save("test save", db_hist_name = 'test_plate_historic.db' ),  "plate test save with 96  added to database plate historic")
        	phi = PlateHist(db_name =  'test_plate_historic.db'  )        	
        	self.assertEqual( str(phi.get_one_hplate(96)),   f'<plate N°1: test save, 96 wells, {phi.date_now}>' )
        
    def test_iteration(self):
    	True
    
    def test_counts(self):
    	True
        	

if __name__ == "__main__":
    unittest.main()
