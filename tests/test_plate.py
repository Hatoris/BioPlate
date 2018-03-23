import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate.Plate import BioPlate
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
        self.plt = BioPlate({"id" : 1}, db_name='test_plate.db')
        self.plt1 = BioPlate(12, 8)
        self.stack = self.plt + self.plt1
        self.Inserts = BioPlate(4, 3, inserts=True)
        self.Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test_Plate_init(self):
        np.testing.assert_array_equal(self.plt,
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['B', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['C', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', '', '', '', '', '', '', '']], dtype='U40'))
        np.testing.assert_array_equal( self.plt1,
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['B', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['C', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', '', '', '', '', '', '', '']], dtype='U40'))
                                                
        np.testing.assert_array_equal(self.Inserts, 
        np.array([[[' ', '1', '2', '3', '4'], 
                        ['A', '', '', '', ''],
                        ['B', '', '', '', ''], 
                        ['C', '', '', '', '']], 
                        [[' ', '1', '2', '3', '4'], 
                        ['A', '', '', '', ''], 
                        ['B', '', '', '', ''], 
                        ['C', '', '', '', '']]], dtype='U40'))
        np.testing.assert_array_equal(self.stack[0], self.plt)
        self.assertIs(self.stack[0], self.plt)
        self.assertIs(self.stack[1], self.plt1)

    #def test_plate_array(self):
        #np.testing.assert_array_equal(self.plt.plate, self.plt.plate_array)

    #def test_matrix_well(self):
        #self.assertEqual(self.plt.matrix_well('A2'), (1, 2))
        #self.assertEqual(self.plt.matrix_well('G7'), (7, 7))

    def test_add_value(self):    
        """
        Test add value on BioPlate from db and BioPlate generated on fly
        """
        np.testing.assert_array_equal(self.plt.add_value("B2", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value("A2", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value("H6", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value("12C", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value("E8", "Test"),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', 'Test', '', '', '', '', '', '', '', '', '', ''],
                                                ['B', '', 'Test', '', '', '', '', '', '', '', '', '', ''],
                                                ['C', '', '', '', '', '', '', '', '', '', '', '', 'Test'],
                                                ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', 'Test', '', '', '', ''],
                                                ['F', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', 'Test', '', '', '', '', '', '']],
                                               dtype='U40'))

        np.testing.assert_array_equal(self.plt1.add_value("B2", "Test"), self.plt1)
        np.testing.assert_array_equal(self.plt1.add_value("A2", "Test"), self.plt1)
        np.testing.assert_array_equal(self.plt1.add_value("H6", "Test"), self.plt1)
        np.testing.assert_array_equal(self.plt1.add_value("12C", "Test"), self.plt1)
        np.testing.assert_array_equal(self.stack.add_value(0, "B8", "Stack")[0], self.plt)
        np.testing.assert_array_equal(self.Inserts.top.add_value( "B3", "inserts"), self.Inserts.top)

    def test_add_value_row(self):
        np.testing.assert_array_equal(self.plt.add_value_row("C[3,12]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value_row("A[4,3]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value_row("F[9,12]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value_row("D[6,8]", 18),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', '', 'Test', 'Test', '', '', '', '', '', '', '', ''],
                                                ['B', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['C', '', '', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test',
                                                 'Test', 'Test', 'Test'],
                                                ['D', '', '', '', '', '', '18', '18', '18', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', '', '', '', '', '', '', '', '', 'Test', 'Test', 'Test', 'Test'],
                                                ['G', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', '', '', '', '', '', '', '']],
                                               dtype='U40'))
        np.testing.assert_array_equal(self.plt.add_value_row("D[1-7]", "Test"), self.plt)
        np.testing.assert_array_equal(self.stack.add_value_row(0, "B[1-6]", "Stack")[0], self.plt)
        np.testing.assert_array_equal(self.Inserts.top.add_value_row( "B[1-3]", "inserts"), self.Inserts.top)     
               
        with self.assertRaises(ValueError) as context:
            self.plt.add_value_row("D[0,8]", 18)
            self.stack.add_value_row(0, "D[0,8]", 18)
            self.Inserts.bot.add_value_row("B[1,6]", 18)

    def test_add_value_column(self):
        np.testing.assert_array_equal(self.plt.add_value_column("3[C,E]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value_column("7[A,H]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value_column("12[F,A]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.add_value_column("1[C,F]", "Test"),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', '', '', '', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['B', '', '', '', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['C', 'Test', '', 'Test', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['D', 'Test', '', 'Test', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['E', 'Test', '', 'Test', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['F', 'Test', '', '', '', '', '', 'Test', '', '', '', '', 'Test'],
                                                ['G', '', '', '', '', '', '', 'Test', '', '', '', '', ''],
                                                ['H', '', '', '', '', '', '', 'Test', '', '', '', '', '']],
                                               dtype='U40'))
        np.testing.assert_array_equal(self.stack.add_value_column(0, "1[B-G]", "Stack")[0], self.plt)
        np.testing.assert_array_equal(self.Inserts.top.add_value_column( "2[A,C]", "inserts"), self.Inserts.top)

    def test_add_values(self):
        V = {"A1": "Test", "B3": "Test"}
        np.testing.assert_array_equal(self.plt.add_values(V), self.plt)
        np.testing.assert_array_equal(self.stack.add_values(0, V)[0], self.plt)
        np.testing.assert_array_equal(self.Inserts.top.add_values(V), self.Inserts.top)

    """
    BIOPlateMatrix

    def test_split_multi_row_column(self):
        self.assertEqual(self.plt.split_multi_row_column('A-E[1,5]'),
                         ['A[1,5]', 'B[1,5]', 'C[1,5]', 'D[1,5]', 'E[1,5]'])
        self.assertEqual(self.plt.split_multi_row_column('1-5[A,E]'),
                         ['1[A,E]', '2[A,E]', '3[A,E]', '4[A,E]', '5[A,E]'])
        self.assertEqual(self.plt.split_multi_row_column('E-A[1,5]'),
                         ['A[1,5]', 'B[1,5]', 'C[1,5]', 'D[1,5]', 'E[1,5]'])
        with self.assertRaises(SyntaxError):
            self.plt.split_multi_row_column('E:A[1,5]')
    """
    def test_add_multi_value(self):
        with self.assertRaises(ValueError):
            self.plt.add_multi_value('A-C[1-5]', ["Test1", "Test2"])
        
        np.testing.assert_array_equal(self.plt.add_multi_value('A-C[1-5]', ["Test1", "Test2", "Test3"]), self.plt)
        np.testing.assert_array_equal(self.plt.add_multi_value('F-H[1-3]', ["Test1", "Test2", "Test3"]),
                                      np.array([[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                                ['A', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1', '', '', '', '', '',
                                                 '', ''],
                                                ['B', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2', '', '', '', '', '',
                                                 '', ''],
                                                ['C', 'Test3', 'Test3', 'Test3', 'Test3', 'Test3', '', '', '', '', '',
                                                 '', ''],
                                                ['D', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['E', '', '', '', '', '', '', '', '', '', '', '', ''],
                                                ['F', 'Test1', 'Test1', 'Test1', '', '', '', '', '', '', '', '', ''],
                                                ['G', 'Test2', 'Test2', 'Test2', '', '', '', '', '', '', '', '', ''],
                                                ['H', 'Test3', 'Test3', 'Test3', '', '', '', '', '', '', '', '', '']],
                                               dtype='U40'))
                                               
        np.testing.assert_array_equal(self.stack.add_multi_value(1,  'F-H[1-3]', ["Test1", "Test2", "Test3"])[1], self.plt1)
        np.testing.assert_array_equal(self.Inserts.top.add_multi_value(  'A-C[1-3]', ["Test1", "Test2", "Test3"] ), self.Inserts.top)

    def test_evaluate(self):
        #matrix
        #with self.assertRaises(SyntaxError):
            #self.plt.evaluate('A:C[1-5]', ["Test1", "Test2", "Test3"])
        np.testing.assert_array_equal(self.plt.evaluate("2[B,E]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.evaluate("A[1,5]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.evaluate("1C", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.evaluate("1-3[A,C]", ["Test1", "Test2", "Test3"]), self.plt)
        np.testing.assert_array_equal(self.plt.evaluate("F-H[1,3]", ["Test1", "Test2", "Test3"]), self.plt)
        np.testing.assert_array_equal(self.stack.evaluate(1,  'F-H[1-3]', ["Test1", "Test2", "Test3"])[1], self.plt1)
        np.testing.assert_array_equal(self.Inserts.top.evaluate(  'A-C[1-3]', ["Test1", "Test2", "Test3"] ), self.Inserts.top)
        
        

    #def test_well_letter_index(self):
       #self.assertEqual(self.plt.well_letter_index("D"), 4)
      #self.assertEqual(self.plt.well_letter_index("H"), 8)

    #def test_letter_index(self):
        #self.assertEqual(self.plt.letter_index("D"), 3)
        #self.assertEqual(self.plt.letter_index("H"), 7)

    #def test_index_letter(self):
        #self.assertEqual(self.plt.index_letter(3), "D")
        #self.assertEqual(self.plt.index_letter(7), "H")

    def test_all_in_one(self):
        v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'],
             'E-G[8,10]': ['Val1', 'Val2', 'Val3']}             
        np.testing.assert_array_equal(self.plt.add_values(v), self.plt)
        self.assertEqual(self.plt.table(), tabulate(self.plt, headers='firstrow'))

    def test_save(self):
        self.plt.add_value('H4', 'Test')
        self.stack.add_value(1, "B6", "test1")
        self.assertEqual(self.plt.save("test save", db_hist_name='test_plate_historic.db'),
                         "BioPlate test save with 96 wells was successfully added to database test_plate_historic.db")
        self.assertEqual(self.stack.save("test save2", db_hist_name='test_plate_historic.db'),
                         "BioPlateStack test save2 with 96 wells was successfully added to database test_plate_historic.db")
        self.assertEqual(self.Inserts.save("test save3", db_hist_name='test_plate_historic.db'),
                         "BioPlateInserts test save3 with 12 wells was successfully added to database test_plate_historic.db")
        phi = PlateHist(db_name='test_plate_historic.db')
        self.assertEqual(str(phi.get_one_hplate(1, key="id")), f'<plate N°1: test save, 96 wells, {phi.date_now}>')
        np.testing.assert_array_equal(phi.get_one_hplate(1, key="id").plate, self.plt)
        np.testing.assert_array_equal(phi.get_one_hplate(2, key="id").plate, self.stack)
        np.testing.assert_array_equal(phi.get_one_hplate(3, key="id").plate, self.Inserts)
        
        

    def test_iteration(self):
        #Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}
        ValIn = {"A1" : "Control", "C[2,4]" : "Test1"}
        self.plt.add_values(self.Value)
        self.Inserts.top.evaluate(ValIn)
        self.assertEqual(list(self.plt.iterate()),
                         [('A1', 'Control'), ('B1', ''), ('C1', ''), ('D1', ''), ('E1', ''), ('F1', ''), ('G1', ''), ('H1', ''), ('A2', ''), ('B2', ''), ('C2', 'Test1'), ('D2', ''), ('E2', ''), ('F2', ''), ('G2', ''), ('H2', ''), ('A3', ''), ('B3', ''), ('C3', 'Test1'), ('D3', ''), ('E3', ''), ('F3', ''), ('G3', ''), ('H3', ''), ('A4', ''), ('B4', ''), ('C4', 'Test1'), ('D4', ''), ('E4', ''), ('F4', ''), ('G4', ''), ('H4', ''), ('A5', ''), ('B5', ''), ('C5', 'Test1'), ('D5', ''), ('E5', ''), ('F5', ''), ('G5', ''), ('H5', ''), ('A6', ''), ('B6', ''), ('C6', 'Test1'), ('D6', ''), ('E6', ''), ('F6', ''), ('G6', ''), ('H6', ''), ('A7', ''), ('B7', ''), ('C7', 'Test1'), ('D7', ''), ('E7', ''), ('F7', ''), ('G7', ''), ('H7', ''), ('A8', ''), ('B8', ''), ('C8', 'Test1'), ('D8', ''), ('E8', ''), ('F8', ''), ('G8', ''), ('H8', ''), ('A9', ''), ('B9', ''), ('C9', 'Test1'), ('D9', ''), ('E9', ''), ('F9', ''), ('G9', ''), ('H9', ''), ('A10', ''), ('B10', ''), ('C10', 'Test1'), ('D10', ''), ('E10', ''), ('F10', ''), ('G10', ''), ('H10', ''), ('A11', ''), ('B11', 'Test2'), ('C11', 'Test2'), ('D11', 'Test2'), ('E11', 'Test2'), ('F11', 'Test2'), ('G11', 'Test2'), ('H11', ''), ('A12', ''), ('B12', ''), ('C12', ''), ('D12', ''), ('E12', ''), ('F12', ''), ('G12', ''), ('H12', '')])
        
        self.assertEqual(list(self.Inserts.iterate()), [('A1', 'Control', ''), ('B1', '', ''), ('C1', '', ''), ('A2', '', ''), ('B2', '', ''), ('C2', 'Test1', ''), ('A3', '', ''), ('B3', '', ''), ('C3', 'Test1', ''), ('A4', '', ''), ('B4', '', ''), ('C4', 'Test1', '')])
        multi = self.plt + self.plt1.add_values(self.Value)
        self.assertEqual(list(multi.iterate(accumulate=True)),
                         [('A1', 'Control', 'Control'), ('B1', '', ''), ('C1', '', ''), ('D1', '', ''), ('E1', '', ''), ('F1', '', ''), ('G1', '', ''), ('H1', '', ''), ('A2', '', ''), ('B2', '', ''), ('C2', 'Test1', 'Test1'), ('D2', '', ''), ('E2', '', ''), ('F2', '', ''), ('G2', '', ''), ('H2', '', ''), ('A3', '', ''), ('B3', '', ''), ('C3', 'Test1', 'Test1'), ('D3', '', ''), ('E3', '', ''), ('F3', '', ''), ('G3', '', ''), ('H3', '', ''), ('A4', '', ''), ('B4', '', ''), ('C4', 'Test1', 'Test1'), ('D4', '', ''), ('E4', '', ''), ('F4', '', ''), ('G4', '', ''), ('H4', '', ''), ('A5', '', ''), ('B5', '', ''), ('C5', 'Test1', 'Test1'), ('D5', '', ''), ('E5', '', ''), ('F5', '', ''), ('G5', '', ''), ('H5', '', ''), ('A6', '', ''), ('B6', '', ''), ('C6', 'Test1', 'Test1'), ('D6', '', ''), ('E6', '', ''), ('F6', '', ''), ('G6', '', ''), ('H6', '', ''), ('A7', '', ''), ('B7', '', ''), ('C7', 'Test1', 'Test1'), ('D7', '', ''), ('E7', '', ''), ('F7', '', ''), ('G7', '', ''), ('H7', '', ''), ('A8', '', ''), ('B8', '', ''), ('C8', 'Test1', 'Test1'), ('D8', '', ''), ('E8', '', ''), ('F8', '', ''), ('G8', '', ''), ('H8', '', ''), ('A9', '', ''), ('B9', '', ''), ('C9', 'Test1', 'Test1'), ('D9', '', ''), ('E9', '', ''), ('F9', '', ''), ('G9', '', ''), ('H9', '', ''), ('A10', '', ''), ('B10', '', ''), ('C10', 'Test1', 'Test1'), ('D10', '', ''), ('E10', '', ''), ('F10', '', ''), ('G10', '', ''), ('H10', '', ''), ('A11', '', ''), ('B11', 'Test2', 'Test2'), ('C11', 'Test2', 'Test2'), ('D11', 'Test2', 'Test2'), ('E11', 'Test2', 'Test2'), ('F11', 'Test2', 'Test2'), ('G11', 'Test2', 'Test2'), ('H11', '', ''), ('A12', '', ''), ('B12', '', ''), ('C12', '', ''), ('D12', '', ''), ('E12', '', ''), ('F12', '', ''), ('G12', '', ''), ('H12', '', '')])
        
        self.assertEqual(list(multi.iterate()), 
            [('A1', 'Control'), ('B1', ''), ('C1', ''), ('D1', ''), ('E1', ''), ('F1', ''), ('G1', ''), ('H1', ''), ('A2', ''), ('B2', ''), ('C2', 'Test1'), ('D2', ''), ('E2', ''), ('F2', ''), ('G2', ''), ('H2', ''), ('A3', ''), ('B3', ''), ('C3', 'Test1'), ('D3', ''), ('E3', ''), ('F3', ''), ('G3', ''), ('H3', ''), ('A4', ''), ('B4', ''), ('C4', 'Test1'), ('D4', ''), ('E4', ''), ('F4', ''), ('G4', ''), ('H4', ''), ('A5', ''), ('B5', ''), ('C5', 'Test1'), ('D5', ''), ('E5', ''), ('F5', ''), ('G5', ''), ('H5', ''), ('A6', ''), ('B6', ''), ('C6', 'Test1'), ('D6', ''), ('E6', ''), ('F6', ''), ('G6', ''), ('H6', ''), ('A7', ''), ('B7', ''), ('C7', 'Test1'), ('D7', ''), ('E7', ''), ('F7', ''), ('G7', ''), ('H7', ''), ('A8', ''), ('B8', ''), ('C8', 'Test1'), ('D8', ''), ('E8', ''), ('F8', ''), ('G8', ''), ('H8', ''), ('A9', ''), ('B9', ''), ('C9', 'Test1'), ('D9', ''), ('E9', ''), ('F9', ''), ('G9', ''), ('H9', ''), ('A10', ''), ('B10', ''), ('C10', 'Test1'), ('D10', ''), ('E10', ''), ('F10', ''), ('G10', ''), ('H10', ''), ('A11', ''), ('B11', 'Test2'), ('C11', 'Test2'), ('D11', 'Test2'), ('E11', 'Test2'), ('F11', 'Test2'), ('G11', 'Test2'), ('H11', ''), ('A12', ''), ('B12', ''), ('C12', ''), ('D12', ''), ('E12', ''), ('F12', ''), ('G12', ''), ('H12', ''), ('A1', 'Control'), ('B1', ''), ('C1', ''), ('D1', ''), ('E1', ''), ('F1', ''), ('G1', ''), ('H1', ''), ('A2', ''), ('B2', ''), ('C2', 'Test1'), ('D2', ''), ('E2', ''), ('F2', ''), ('G2', ''), ('H2', ''), ('A3', ''), ('B3', ''), ('C3', 'Test1'), ('D3', ''), ('E3', ''), ('F3', ''), ('G3', ''), ('H3', ''), ('A4', ''), ('B4', ''), ('C4', 'Test1'), ('D4', ''), ('E4', ''), ('F4', ''), ('G4', ''), ('H4', ''), ('A5', ''), ('B5', ''), ('C5', 'Test1'), ('D5', ''), ('E5', ''), ('F5', ''), ('G5', ''), ('H5', ''), ('A6', ''), ('B6', ''), ('C6', 'Test1'), ('D6', ''), ('E6', ''), ('F6', ''), ('G6', ''), ('H6', ''), ('A7', ''), ('B7', ''), ('C7', 'Test1'), ('D7', ''), ('E7', ''), ('F7', ''), ('G7', ''), ('H7', ''), ('A8', ''), ('B8', ''), ('C8', 'Test1'), ('D8', ''), ('E8', ''), ('F8', ''), ('G8', ''), ('H8', ''), ('A9', ''), ('B9', ''), ('C9', 'Test1'), ('D9', ''), ('E9', ''), ('F9', ''), ('G9', ''), ('H9', ''), ('A10', ''), ('B10', ''), ('C10', 'Test1'), ('D10', ''), ('E10', ''), ('F10', ''), ('G10', ''), ('H10', ''), ('A11', ''), ('B11', 'Test2'), ('C11', 'Test2'), ('D11', 'Test2'), ('E11', 'Test2'), ('F11', 'Test2'), ('G11', 'Test2'), ('H11', ''), ('A12', ''), ('B12', ''), ('C12', ''), ('D12', ''), ('E12', ''), ('F12', ''), ('G12', ''), ('H12', '')])

    def test_count(self):
        #Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}
        ValIn = {"A1" : "Control", "C[2,4]" : "Test1"}
        self.plt.add_values(self.Value)
        self.Inserts.top.add_values(ValIn)
        self.assertEqual(self.plt.count(), {'': 80, 'Control': 1, 'Test1': 9, 'Test2': 6})
        multi = self.plt + self.plt1.add_values(self.Value)
        multiInsert = self.Inserts + BioPlate(4,  3, inserts = True)
        self.assertEqual(multi.count(),
                         {0: {'': 80, 'Control': 1, 'Test1': 9, 'Test2': 6},
                          1: {'': 80, 'Control': 1, 'Test1': 9, 'Test2': 6}})
        self.assertEqual(self.Inserts.count(), {'top': {'Control': 1, 'Test1': 3, '': 8}, 'bot': {'': 12}})
        self.assertEqual(multiInsert.count(), 
        {0: {'top': {'Control': 1, 'Test1': 3, '': 8}, 'bot': {'': 12}}, 
        1: {'top': {'': 12}, 'bot': {'': 12}}})
        
    def test_get_value(self):
        self.plt.evaluate(self.Value)
        self.Inserts.top.add_value("C2", "Test1")
        np.testing.assert_array_equal(self.plt.get_value( "C2"), 'Test1')
        np.testing.assert_array_equal(self.stack.get_value(0, "C2"), 'Test1')
        np.testing.assert_array_equal(self.Inserts.top.get_value("C2"), 'Test1')

    def test_get_value_row(self):
         self.plt.evaluate(self.Value)
         np.testing.assert_array_equal(self.plt.get_value_row("C[1,6]"), ['', "Test1", "Test1", "Test1", "Test1", "Test1" ])
        
    def test_get_value_column(self):
        pass
        
    def test_get_values(self):
        pass

if __name__ == "__main__":
    unittest.main()
