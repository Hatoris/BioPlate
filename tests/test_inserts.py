import unittest
import contextlib
from string import ascii_uppercase
from pathlib import Path, PurePath

import numpy as np
from tabulate import tabulate

from BioPlate import BioPlate
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
import BioPlate.core.utilitis as bpu


class TestInserts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
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
        self.Ins = BioPlate({"id": 1}, db_name="test_plate.db", inserts=True)
        self.Inserts = BioPlate(4, 3, inserts=True)
        self.Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        try:
            Path(PurePath("test_ins_to_excel.xlsx")).unlink()
        except FileNotFoundError:
            pass
           
           
    def test_Plate_init(self):
        np.testing.assert_array_equal(
            self.Inserts,
            np.array(
                [
                    [
                        ["", "1", "2", "3", "4"],
                        ["A", "", "", "", ""],
                        ["B", "", "", "", ""],
                        ["C", "", "", "", ""],
                    ],
                    [
                        ["", "1", "2", "3", "4"],
                        ["A", "", "", "", ""],
                        ["B", "", "", "", ""],
                        ["C", "", "", "", ""],
                    ],
                ],
                dtype="U40",
            ),
        )
        
    def test_add_values(self):
        np.testing.assert_array_equal(
            self.Inserts.top.set("B3", "inserts"), self.Inserts.top
        )
        np.testing.assert_array_equal(
            self.Inserts.bot.set("B3", "inserts_bot"), self.Inserts.bot
        )
        self.Inserts["top", "A2"] = "Bob"
        self.assertEqual(self.Inserts[0, "A2"], "Bob")
        self.Inserts["bot", "A2"] = "Bibi"
        self.assertEqual(self.Inserts[1, "A2"], "Bibi")

    def test_add_list(self):
        self.Inserts["top", "A[1-3]"] = ["b1", "b2", "b3"]
        self.assertEqual(self.Inserts[0, "A1"], "b1")

    def test_add_value_row(self):
        np.testing.assert_array_equal(
            self.Inserts.top.set("B[1-3]", "inserts"), self.Inserts.top
        )
        np.testing.assert_array_equal(
            self.Inserts.bot.set("A", "inserts"), self.Inserts.bot
        )
        np.testing.assert_array_equal(
            self.Inserts.bot.set("B", "inserts2"), self.Inserts.bot
        )
        np.testing.assert_array_equal(
            self.Inserts.bot.set("B[1,6]", 18), self.Inserts.bot) 
    
    def test_add_value_column(self):
        np.testing.assert_array_equal(
            self.Inserts.top.set("2[A,C]", "inserts"), self.Inserts.top
        )
        np.testing.assert_array_equal(
            self.Inserts.top.set("B", "inserts2"), self.Inserts.top
        )

    def test_set(self):
        with self.assertRaises(IndexError):
            self.Inserts.top.set(self.Value)
        with self.assertRaises(ValueError):
           self.Inserts.bot.set("A[2-4]", ["test1", "test2", "test3", "test4"])
        np.testing.assert_array_equal(
            self.Inserts.top.set("A-C[1-3]", ["Test1", "Test2", "Test3"]),
            self.Inserts.top,
        )
        Ns = BioPlate(12, 8, inserts=True)
        Ns["bot", "4-7[A-D]"] = ["boom1", "boom2", "boom3", "boom4"]
        np.testing.assert_array_equal(Ns["bot", "4-7[A-D]"], np.array([["boom1", "boom2", "boom3", "boom4"],
                   ["boom1", "boom2", "boom3", "boom4"],
                   ["boom1", "boom2", "boom3", "boom4"],
                   ["boom1", "boom2", "boom3", "boom4"]]))                

    def test_table(self):
        v = {
            "A[2,8]": "VC",
            "H[2,8]": "MS",
            "1-4[B,G]": ["MLR", "NT", "1.1", "1.2"],
            "E-G[8,10]": ["Val1", "Val2", "Val3"],
        }
        np.testing.assert_array_equal(self.Ins.top.set(v), self.Ins.top)
        self.assertEqual(self.Ins.top.table(), tabulate(self.Ins.top, headers="firstrow"))                                                          
    def test_save(self):
        self.assertEqual(
            self.Inserts.save("test save3", db_hist_name="test_plate_historic.db"),
            "Inserts test save3 with 12 wells was successfully added to database test_plate_historic.db",
        )
        phi = PlateHist(db_name="test_plate_historic.db")
        np.testing.assert_array_equal(
            phi.get_one_hplate(1, key="id").plate, self.Inserts
        )
    def test_iteration(self):
       ValIn = {"A1": "Control", "C[2,4]": "Test1"}
       self.Inserts.top.set(ValIn)
       self.assertEqual(
            list(self.Inserts.iterate()),
            [
                ("A1", "Control", ""),
                ("B1", "", ""),
                ("C1", "", ""),
                ("A2", "", ""),
                ("B2", "", ""),
                ("C2", "Test1", ""),
                ("A3", "", ""),
                ("B3", "", ""),
                ("C3", "Test1", ""),
                ("A4", "", ""),
                ("B4", "", ""),
                ("C4", "Test1", ""),
            ],
        )
        
    def test_count(self):
        ValIn = {"A1": "Control", "C[2,4]": "Test1"}
        self.Inserts.top.set(ValIn)
        self.assertEqual(
                self.Inserts.count(),
                {"top": {"Control": 1, "Test1": 3, "": 8}, "bot": {"": 12}},
            )
         
    def test_get_value(self):
        self.Inserts.top.set("C2", "Test1")
        np.testing.assert_array_equal( self.Inserts.top.get("C2"), "Test1")
        
    def test_get_values(self):
        self.Inserts.bot.set("A[1-3]", ["bob1", "bob2", "bob3"])
        self.Inserts.bot["B[1-3]"] =  ["bibi1", "bibi2", "bibi3"]
        self.assertEqual(
            self.Inserts.bot.get("A1", "2[A-B]"), ["bob1", ["bob2", "bibi2"]]
        )
    
    def test_name(self):
        self.assertEqual(self.Inserts.name, "Inserts")
        self.assertEqual(self.Ins.name, "Inserts")
        
    def test_to_excel(self):
        self.Inserts.to_excel("test_ins_to_excel.xlsx")
        exist_ins = Path("test_ins_to_excel.xlsx").exists()
        self.assertTrue(exist_ins)
        
    def test_merge(self):
        ins = BioPlate(12, 8, inserts=True)
        ins.top.set("2-5[A-C]", ["test", "tes", "te", "t"])
        self.assertEqual(ins.top.get("A2"), "test")
        ins.top.set("2-3[A-C]", ["_1", "_2"], merge=True)
        ins.top.set("A-C[4-5]", ["_3", "_4", "_5"], merge=True)
        self.assertEqual(ins.top.get("A2"), "test_1")
        self.assertEqual(ins.top.get("B3"), "tes_2")
        self.assertEqual(ins.top.get("A4"), "te_3")
        self.assertEqual(ins.top.get("B5"), "t_4")
        self.assertEqual(ins.top.get("C5"), "t_5")
        
    def test_raise_inserts(self):
        with self.assertRaises(ValueError):
            self.Inserts.set("A5", "martin")
            
    def test_insert_set_get(self):
        ii = BioPlate(12, 8, inserts=True)
        ii["top", "A[3-7]"] = "Bob"
        ii["bot", "B-D[6-9]"] = ["t1", "t2", "t3"]
        ii[0, "7-10[F-H]"] = ["t4", "t5", "t6", "t7"]
        self.assertEqual(ii.top.get("A4" ), "Bob")
        self.assertEqual(ii.bot.get("C7" ), "t2")
        self.assertEqual(ii.top.get("G8" ), "t5")
        self.assertEqual(ii["top", "A5"], "Bob")
        self.assertEqual(ii["bot", "B6"], "t1")
        self.assertEqual(ii[0, "H10"], "t7")
        self.assertEqual(ii[1, 3, 8], "t2")
                          
if __name__ == "__main__":
    unittest.main()