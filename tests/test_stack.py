import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from BioPlate import BioPlate
from BioPlate.stack import BioPlateStack
from string import ascii_uppercase
from tabulate import tabulate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist


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
        cls.plt3 = BioPlate(12, 8)
        cls.plt3.set("A1", "plt3")
        cls.Ins = BioPlate(12, 8, inserts=True)
        cls.Ins.top.set("A1", "topIns")
        cls.Ins1 = BioPlate(12, 8, inserts=True)
        cls.Ins1.top.set("A1", "topIns1")
        cls.pdb = PlateDB(db_name="test_plate.db")
        cls.pdb.add_plate(
            numWell=96,
            numColumns=12,
            numRows=8,
            surfWell=0.29,
            maxVolWell=200,
            workVolWell=200,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )

    @classmethod
    def tearDownClass(cls):
        """
        This function is run one time at the end of tests
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(
                PurePath(
                    Path(__file__).parent.parent,
                    "BioPlate/database/DBFiles",
                    "test_plate.db",
                )
            ).unlink()
            Path(
                PurePath(
                    Path(__file__).parent.parent,
                    "BioPlate/database/DBFiles",
                    "test_plate_historic.db",
                )
            ).unlink()
            Path(
                PurePath(
                    Path(__file__).parent.parent,
                    "BioPlate/database/DBFiles",
                    "plate_historic.db",
                )
            ).unlink()

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.stack = self.plt + self.plt1
        self.stack1 = BioPlate(4, 12, 8)
        self.stacki = self.Ins + self.Ins1
        self.stacki1 = BioPlate(4, 12, 8, inserts=True)
        self.Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}
        

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        try:
            Path(PurePath("test_stack_to_excel.xlsx")).unlink()
        except FileNotFoundError:
            pass

    def test_init_(self):
        np.testing.assert_array_equal(self.stack[0], self.plt)
        self.assertIs(self.stack[0], self.plt)
        self.assertIs(self.stack[1], self.plt1)

    def test_add_value(self):
        np.testing.assert_array_equal(self.stack.set(0, "B8", "Stack")[0], self.plt)

    def test_add_value_row(self):
        np.testing.assert_array_equal(self.stack.set(0, "B[1-6]", "Stack")[0], self.plt)
        with self.assertRaises(ValueError) as context:
            self.stack.set(0, "D[0,8]", 18)
    
    def test_add_value_column(self):
        np.testing.assert_array_equal(self.stack.set(0, "1[B-G]", "Stack")[0], self.plt)    

    def test_set(self):
        V = {"A1": "Test", "B3": "Test"}
        np.testing.assert_array_equal(self.stack.set(0, V)[0], self.plt)
        with self.assertRaises(IndexError):
            self.stack.set(3, "A6", "tutu")
        np.testing.assert_array_equal(
            self.stack.set(1, "F-H[1-3]", ["Test1", "Test2", "Test3"])[1], self.plt1
        )
        np.testing.assert_array_equal(
            self.stack.set(1, "F-H[1-3]", ["Test1", "Test2", "Test3"])[1], self.plt1
        )

    def test_all_in_one(self):
        v = {
            "A[2,8]": "VC",
            "H[2,8]": "MS",
            "1-4[B,G]": ["MLR", "NT", "1.1", "1.2"],
            "E-G[8,10]": ["Val1", "Val2", "Val3"],
        }        
        np.testing.assert_array_equal(self.stack[0].set(v), self.plt)
        self.assertEqual(self.stack[0].table(), tabulate(self.stack[0], headers="firstrow"))

    def test_save(self):
        self.stack.set(1, "B6", "test1")                                
        self.assertEqual(
            self.stack.save("test save2", db_hist_name="test_plate_historic.db"),
            "BioPlateStack test save2 with 96 wells was successfully added to database test_plate_historic.db",
        )
        self.assertEqual(
            self.stack.save("test save2"),
            "BioPlateStack test save2 with 96 wells was successfully added to database plate_historic.db",
        )
        phi = PlateHist(db_name="test_plate_historic.db")
        np.testing.assert_array_equal( phi.get_one_hplate( 1, key="id").plate, self.stack)
        
    def test_iteration(self):
        pltx = BioPlate(12, 8)
        plti = BioPlate(12, 8)
        plti.set(self.Value)
        multi = plti + pltx.set(self.Value)
        self.assertEqual(
            list(multi.iterate(accumulate=True)),
            [
                ("A1", "Control", "Control"),
                ("B1", "", ""),
                ("C1", "", ""),
                ("D1", "", ""),
                ("E1", "", ""),
                ("F1", "", ""),
                ("G1", "", ""),
                ("H1", "", ""),
                ("A2", "", ""),
                ("B2", "", ""),
                ("C2", "Test1", "Test1"),
                ("D2", "", ""),
                ("E2", "", ""),
                ("F2", "", ""),
                ("G2", "", ""),
                ("H2", "", ""),
                ("A3", "", ""),
                ("B3", "", ""),
                ("C3", "Test1", "Test1"),
                ("D3", "", ""),
                ("E3", "", ""),
                ("F3", "", ""),
                ("G3", "", ""),
                ("H3", "", ""),
                ("A4", "", ""),
                ("B4", "", ""),
                ("C4", "Test1", "Test1"),
                ("D4", "", ""),
                ("E4", "", ""),
                ("F4", "", ""),
                ("G4", "", ""),
                ("H4", "", ""),
                ("A5", "", ""),
                ("B5", "", ""),
                ("C5", "Test1", "Test1"),
                ("D5", "", ""),
                ("E5", "", ""),
                ("F5", "", ""),
                ("G5", "", ""),
                ("H5", "", ""),
                ("A6", "", ""),
                ("B6", "", ""),
                ("C6", "Test1", "Test1"),
                ("D6", "", ""),
                ("E6", "", ""),
                ("F6", "", ""),
                ("G6", "", ""),
                ("H6", "", ""),
                ("A7", "", ""),
                ("B7", "", ""),
                ("C7", "Test1", "Test1"),
                ("D7", "", ""),
                ("E7", "", ""),
                ("F7", "", ""),
                ("G7", "", ""),
                ("H7", "", ""),
                ("A8", "", ""),
                ("B8", "", ""),
                ("C8", "Test1", "Test1"),
                ("D8", "", ""),
                ("E8", "", ""),
                ("F8", "", ""),
                ("G8", "", ""),
                ("H8", "", ""),
                ("A9", "", ""),
                ("B9", "", ""),
                ("C9", "Test1", "Test1"),
                ("D9", "", ""),
                ("E9", "", ""),
                ("F9", "", ""),
                ("G9", "", ""),
                ("H9", "", ""),
                ("A10", "", ""),
                ("B10", "", ""),
                ("C10", "Test1", "Test1"),
                ("D10", "", ""),
                ("E10", "", ""),
                ("F10", "", ""),
                ("G10", "", ""),
                ("H10", "", ""),
                ("A11", "", ""),
                ("B11", "Test2", "Test2"),
                ("C11", "Test2", "Test2"),
                ("D11", "Test2", "Test2"),
                ("E11", "Test2", "Test2"),
                ("F11", "Test2", "Test2"),
                ("G11", "Test2", "Test2"),
                ("H11", "", ""),
                ("A12", "", ""),
                ("B12", "", ""),
                ("C12", "", ""),
                ("D12", "", ""),
                ("E12", "", ""),
                ("F12", "", ""),
                ("G12", "", ""),
                ("H12", "", ""),
            ],
        )
        self.assertEqual(
            list(multi.iterate(accumulate=False)),
            [
                ("A1", "Control"),
                ("B1", ""),
                ("C1", ""),
                ("D1", ""),
                ("E1", ""),
                ("F1", ""),
                ("G1", ""),
                ("H1", ""),
                ("A2", ""),
                ("B2", ""),
                ("C2", "Test1"),
                ("D2", ""),
                ("E2", ""),
                ("F2", ""),
                ("G2", ""),
                ("H2", ""),
                ("A3", ""),
                ("B3", ""),
                ("C3", "Test1"),
                ("D3", ""),
                ("E3", ""),
                ("F3", ""),
                ("G3", ""),
                ("H3", ""),
                ("A4", ""),
                ("B4", ""),
                ("C4", "Test1"),
                ("D4", ""),
                ("E4", ""),
                ("F4", ""),
                ("G4", ""),
                ("H4", ""),
                ("A5", ""),
                ("B5", ""),
                ("C5", "Test1"),
                ("D5", ""),
                ("E5", ""),
                ("F5", ""),
                ("G5", ""),
                ("H5", ""),
                ("A6", ""),
                ("B6", ""),
                ("C6", "Test1"),
                ("D6", ""),
                ("E6", ""),
                ("F6", ""),
                ("G6", ""),
                ("H6", ""),
                ("A7", ""),
                ("B7", ""),
                ("C7", "Test1"),
                ("D7", ""),
                ("E7", ""),
                ("F7", ""),
                ("G7", ""),
                ("H7", ""),
                ("A8", ""),
                ("B8", ""),
                ("C8", "Test1"),
                ("D8", ""),
                ("E8", ""),
                ("F8", ""),
                ("G8", ""),
                ("H8", ""),
                ("A9", ""),
                ("B9", ""),
                ("C9", "Test1"),
                ("D9", ""),
                ("E9", ""),
                ("F9", ""),
                ("G9", ""),
                ("H9", ""),
                ("A10", ""),
                ("B10", ""),
                ("C10", "Test1"),
                ("D10", ""),
                ("E10", ""),
                ("F10", ""),
                ("G10", ""),
                ("H10", ""),
                ("A11", ""),
                ("B11", "Test2"),
                ("C11", "Test2"),
                ("D11", "Test2"),
                ("E11", "Test2"),
                ("F11", "Test2"),
                ("G11", "Test2"),
                ("H11", ""),
                ("A12", ""),
                ("B12", ""),
                ("C12", ""),
                ("D12", ""),
                ("E12", ""),
                ("F12", ""),
                ("G12", ""),
                ("H12", ""),
                ("A1", "Control"),
                ("B1", ""),
                ("C1", ""),
                ("D1", ""),
                ("E1", ""),
                ("F1", ""),
                ("G1", ""),
                ("H1", ""),
                ("A2", ""),
                ("B2", ""),
                ("C2", "Test1"),
                ("D2", ""),
                ("E2", ""),
                ("F2", ""),
                ("G2", ""),
                ("H2", ""),
                ("A3", ""),
                ("B3", ""),
                ("C3", "Test1"),
                ("D3", ""),
                ("E3", ""),
                ("F3", ""),
                ("G3", ""),
                ("H3", ""),
                ("A4", ""),
                ("B4", ""),
                ("C4", "Test1"),
                ("D4", ""),
                ("E4", ""),
                ("F4", ""),
                ("G4", ""),
                ("H4", ""),
                ("A5", ""),
                ("B5", ""),
                ("C5", "Test1"),
                ("D5", ""),
                ("E5", ""),
                ("F5", ""),
                ("G5", ""),
                ("H5", ""),
                ("A6", ""),
                ("B6", ""),
                ("C6", "Test1"),
                ("D6", ""),
                ("E6", ""),
                ("F6", ""),
                ("G6", ""),
                ("H6", ""),
                ("A7", ""),
                ("B7", ""),
                ("C7", "Test1"),
                ("D7", ""),
                ("E7", ""),
                ("F7", ""),
                ("G7", ""),
                ("H7", ""),
                ("A8", ""),
                ("B8", ""),
                ("C8", "Test1"),
                ("D8", ""),
                ("E8", ""),
                ("F8", ""),
                ("G8", ""),
                ("H8", ""),
                ("A9", ""),
                ("B9", ""),
                ("C9", "Test1"),
                ("D9", ""),
                ("E9", ""),
                ("F9", ""),
                ("G9", ""),
                ("H9", ""),
                ("A10", ""),
                ("B10", ""),
                ("C10", "Test1"),
                ("D10", ""),
                ("E10", ""),
                ("F10", ""),
                ("G10", ""),
                ("H10", ""),
                ("A11", ""),
                ("B11", "Test2"),
                ("C11", "Test2"),
                ("D11", "Test2"),
                ("E11", "Test2"),
                ("F11", "Test2"),
                ("G11", "Test2"),
                ("H11", ""),
                ("A12", ""),
                ("B12", ""),
                ("C12", ""),
                ("D12", ""),
                ("E12", ""),
                ("F12", ""),
                ("G12", ""),
                ("H12", ""),
            ],
        )

    def test_count(self):
        ValIn = {"A1": "Control", "C[2,4]": "Test1"}
        multi = BioPlate(2, 12, 8)
        multi.set(0, self.Value)
        multi.set(1, self.Value)
        multiinserts = BioPlate(2, 4, 3, inserts=True)
        multiinserts.set(0, "top", ValIn)
        self.assertEqual(
            multi.count(),
            {
                0: {"": 80, "Control": 1, "Test1": 9, "Test2": 6},
                1: {"": 80, "Control": 1, "Test1": 9, "Test2": 6},
            },
        )
        self.assertEqual(
            multiinserts.count(),
            {
                0: {"top": {"Control": 1, "Test1": 3, "": 8}, "bot": {"": 12}},
                1: {"top": {"": 12}, "bot": {"": 12}},
            },
        )

    def test_get_value(self):
        np.testing.assert_array_equal(self.stack.get(0, "C2"), "NT")

    def test_name(self):
        self.assertEqual(self.stack.name, "BioPlateStack")

    def test_to_excel(self):
        self.stack.to_excel("test_stack_to_excel.xlsx")
        exist_stack = Path("test_stack_to_excel.xlsx").exists()
        self.assertTrue(exist_stack)

    def test_merge(self):
        self.stack.set(0, "A3", "_bob", merge=True)
        self.assertEqual(self.stack.get(0, "A3"), "VC_bob")

    def test_inserts_stack(self):
        ins = BioPlate(2, 12, 8, inserts=True)
        ins.set(0, "top", "A1", "gaston")
        ins1 = BioPlate(2, 12, 8, inserts=True)
        ins1.set(0, "bot",  "A1", "gulu")
        ins2 = BioPlate(12, 8, inserts=True)
        Nins = ins + ins1
        PNins = ins2 + ins
        self.assertEqual(Nins.get(0, "top", "A1"), "gaston")
        self.assertEqual(Nins.get(2, "bot", "A1"), "gulu")
        self.assertEqual(PNins.get(1, "top", "A1"), "gaston")

    def test__repr__(self):
        self.maxDiff = None
        self.assertEqual(str(self.stack), str(np.array([self.plt, self.plt1])))

    def test__setitem__(self):
        self.stack[0, 1, 2] = "testset"
        self.assertEqual(self.stack[0][1, 2], "testset")

    def test__add__(self):
        Nstack = self.stack + self.plt2
        self.assertEqual(Nstack.name, "BioPlateStack")
        np.testing.assert_array_equal(Nstack[2], self.plt2)
        with self.assertRaises(ValueError):
            Nstack + self.plt2
        N2stack = self.plt2 + self.plt3
        Astack = self.stack + N2stack
        np.testing.assert_array_equal(Nstack[2], self.plt2)
        pp = BioPlate(12, 8)
        ps = BioPlate(2, 12, 8)
        Nps = pp + ps
        self.assertIs(Nps[0], pp)

    def test_change_args(self):
        Nstacki = self.Ins + self.Ins1
        self.assertEqual(Nstacki.get(0, "top", "A1"), "topIns")

    def test_getitem(self):
        self.assertEqual(self.stack[0, "A1"],  "test")
        self.assertEqual(self.stacki[0, "top", "A1" ],  "topIns")
        self.assertEqual(self.stack[0,1, 1], "test")
        
    def test_setitem(self):
        self.stack[0, "B2"] = "bob"
        self.assertEqual(self.stack.get(0, "B2"), "bob")
        self.stacki[1, "bot", "B[6-9]"] = "marmite"
        self.assertEqual(self.stacki.get(1, "bot", "B7"), "marmite")
       
        
if __name__ == "__main__":
    unittest.main()
