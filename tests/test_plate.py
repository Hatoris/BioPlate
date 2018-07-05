import unittest
import contextlib
import numpy as np
import BioPlate.utilitis as bpu

from pathlib import Path, PurePath
from BioPlate import BioPlate
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
        self.plt = BioPlate({"id": 1}, db_name="test_plate.db")
        self.plt1 = BioPlate(12, 8)
        self.Value = {"A1": "Control", "C[2,10]": "Test1", "11[B,G]": "Test2"}

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        try:
            Path(PurePath("test_plate_to_excel.xlsx")).unlink()
            Path(PurePath("test_stack_to_excel.xlsx")).unlink()
        except FileNotFoundError:
            pass

    def test_Plate_init(self):
        np.testing.assert_array_equal(
            self.plt,
            np.array(
                [
                    [
                        " ",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                    ],
                    ["A", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["B", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["C", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["D", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["E", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["F", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["G", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["H", "", "", "", "", "", "", "", "", "", "", "", ""],
                ],
                dtype="U40",
            ),
        )
        np.testing.assert_array_equal(
            self.plt1,
            np.array(
                [
                    [
                        " ",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                    ],
                    ["A", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["B", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["C", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["D", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["E", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["F", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["G", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["H", "", "", "", "", "", "", "", "", "", "", "", ""],
                ],
                dtype="U40",
            ),
        )

    def test_add_value(self):
        """
        Test add value on BioPlate from db and BioPlate generated on fly
        """
        np.testing.assert_array_equal(self.plt.set("B2", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("A2", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("H6", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("12C", "Test"), self.plt)
        np.testing.assert_array_equal(
            self.plt.set("E8", "Test"),
            np.array(
                [
                    [
                        " ",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                    ],
                    ["A", "", "Test", "", "", "", "", "", "", "", "", "", ""],
                    ["B", "", "Test", "", "", "", "", "", "", "", "", "", ""],
                    ["C", "", "", "", "", "", "", "", "", "", "", "", "Test"],
                    ["D", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["E", "", "", "", "", "", "", "", "Test", "", "", "", ""],
                    ["F", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["G", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["H", "", "", "", "", "", "Test", "", "", "", "", "", ""],
                ],
                dtype="U40",
            ),
        )

        np.testing.assert_array_equal(self.plt1.set("B2", "Test"), self.plt1)
        np.testing.assert_array_equal(self.plt1.set("A2", "Test"), self.plt1)
        np.testing.assert_array_equal(self.plt1.set("H6", "Test"), self.plt1)
        np.testing.assert_array_equal(self.plt1.set("12C", "Test"), self.plt1)


    def test_add_value_row(self):
        np.testing.assert_array_equal(self.plt.set("C[3,12]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("A[4,3]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("F[9,12]", "Test"), self.plt)
        np.testing.assert_array_equal(
            self.plt.set("D[6,8]", 18),
            np.array(
                [
                    [
                        " ",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                    ],
                    ["A", "", "", "Test", "Test", "", "", "", "", "", "", "", ""],
                    ["B", "", "", "", "", "", "", "", "", "", "", "", ""],
                    [
                        "C",
                        "",
                        "",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                    ],
                    ["D", "", "", "", "", "", "18", "18", "18", "", "", "", ""],
                    ["E", "", "", "", "", "", "", "", "", "", "", "", ""],
                    [
                        "F",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "Test",
                        "Test",
                        "Test",
                        "Test",
                    ],
                    ["G", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["H", "", "", "", "", "", "", "", "", "", "", "", ""],
                ],
                dtype="U40",
            ),
        )
        np.testing.assert_array_equal(self.plt.set("D[1-7]", "Test"), self.plt)
        with self.assertRaises(ValueError) as context:
            self.plt.set("D[0,8]", 18)

    def test_add_value_column(self):
        np.testing.assert_array_equal(self.plt.set("3[C,E]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("7[A,H]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("12[F,A]", "Test"), self.plt)
        np.testing.assert_array_equal(
            self.plt.set("1[C,F]", "Test"),
            np.array(
                [
                    [
                        " ",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                    ],
                    ["A", "", "", "", "", "", "", "Test", "", "", "", "", "Test"],
                    ["B", "", "", "", "", "", "", "Test", "", "", "", "", "Test"],
                    [
                        "C",
                        "Test",
                        "",
                        "Test",
                        "",
                        "",
                        "",
                        "Test",
                        "",
                        "",
                        "",
                        "",
                        "Test",
                    ],
                    [
                        "D",
                        "Test",
                        "",
                        "Test",
                        "",
                        "",
                        "",
                        "Test",
                        "",
                        "",
                        "",
                        "",
                        "Test",
                    ],
                    [
                        "E",
                        "Test",
                        "",
                        "Test",
                        "",
                        "",
                        "",
                        "Test",
                        "",
                        "",
                        "",
                        "",
                        "Test",
                    ],
                    ["F", "Test", "", "", "", "", "", "Test", "", "", "", "", "Test"],
                    ["G", "", "", "", "", "", "", "Test", "", "", "", "", ""],
                    ["H", "", "", "", "", "", "", "Test", "", "", "", "", ""],
                ],
                dtype="U40",
            ),
        )

    def test_set(self):
        V = {"A1": "Test", "B3": "Test"}
        np.testing.assert_array_equal(self.plt.set(V), self.plt)

    def test_set_again(self):
        with self.assertRaises(ValueError):
            self.plt.set("A-C[1-5]", ["Test1", "Test2"])
            self.plt.set("A2", ["tezt1", "test2"])
        np.testing.assert_array_equal(
            self.plt.set("A-C[1-5]", ["Test1", "Test2", "Test3"]), self.plt
        )
        np.testing.assert_array_equal(
            self.plt.set("F-H[1-3]", ["Test1", "Test2", "Test3"]),
            np.array(
                [
                    [
                        " ",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                    ],
                    [
                        "A",
                        "Test1",
                        "Test1",
                        "Test1",
                        "Test1",
                        "Test1",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                    [
                        "B",
                        "Test2",
                        "Test2",
                        "Test2",
                        "Test2",
                        "Test2",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                    [
                        "C",
                        "Test3",
                        "Test3",
                        "Test3",
                        "Test3",
                        "Test3",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                    ["D", "", "", "", "", "", "", "", "", "", "", "", ""],
                    ["E", "", "", "", "", "", "", "", "", "", "", "", ""],
                    [
                        "F",
                        "Test1",
                        "Test1",
                        "Test1",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                    [
                        "G",
                        "Test2",
                        "Test2",
                        "Test2",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                    [
                        "H",
                        "Test3",
                        "Test3",
                        "Test3",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                ],
                dtype="U40",
            ),
        )

    def test_set(self):
        np.testing.assert_array_equal(self.plt.set("2[B,E]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("A[1,5]", "Test"), self.plt)
        np.testing.assert_array_equal(self.plt.set("1C", "Test"), self.plt)
        np.testing.assert_array_equal(
            self.plt.set("1-3[A,C]", ["Test1", "Test2", "Test3"]), self.plt
        )
        np.testing.assert_array_equal(
            self.plt.set("F-H[1,3]", ["Test1", "Test2", "Test3"]), self.plt
        )
        np.testing.assert_array_equal(self.plt.set("A-D[1,3]", "Test4"), self.plt)

    def test_all_in_one(self):
        v = {
            "A[2,8]": "VC",
            "H[2,8]": "MS",
            "1-4[B,G]": ["MLR", "NT", "1.1", "1.2"],
            "E-G[8,10]": ["Val1", "Val2", "Val3"],
        }
        np.testing.assert_array_equal(self.plt.set(v), self.plt)
        self.assertEqual(self.plt.table(), tabulate(self.plt, headers="firstrow"))

    def test_save(self):
        self.plt.set("H4", "Test")
        self.assertEqual(
            self.plt.save("test save", db_hist_name="test_plate_historic.db"),
            "Plate test save with 96 wells was successfully added to database test_plate_historic.db",
        )
        self.plt.set("H5", "lol")
        self.assertEqual(
            self.plt.save("test save", db_hist_name="test_plate_historic.db"),
            "plate with 1 id updated",
        )
        phi = PlateHist(db_name="test_plate_historic.db")
        self.assertEqual(
            str(phi.get_one_hplate(1, key="id")),
            f"<plate N°1: test save, 96 wells, {phi.date_now}>",
        )
        np.testing.assert_array_equal(phi.get_one_hplate(1, key="id").plate, self.plt)

    def test_iteration(self):
        ValIn = {"A1": "Control", "C[2,4]": "Test1"}
        self.plt.set(self.Value)
        self.assertEqual(
            list(self.plt.iterate()),
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
            ],
        ) 

    def test_count(self):
        ValIn = {"A1": "Control", "C[2,4]": "Test1"}
        self.plt.set(self.Value)
        self.assertEqual(
            self.plt.count(), {"": 80, "Control": 1, "Test1": 9, "Test2": 6}
        )

    def test_get_value(self):
        self.plt.set(self.Value)
        np.testing.assert_array_equal(self.plt.get("C2"), "Test1")

    def test_get_value_row(self):
        self.plt.set(self.Value)
        np.testing.assert_array_equal(
            self.plt.get("C[1,6]"), ["", "Test1", "Test1", "Test1", "Test1", "Test1"]
        )

    def test_get_values(self):
        self.plt.set(self.Value)
        self.assertEqual(
            self.plt.get("A1", "B[1-6]"), ["Control", ["", "", "", "", "", ""]]
        )
        self.assertEqual(self.plt.get("A1"), "Control")
        np.testing.assert_array_equal(
            self.plt.get(1), ["Control", "", "", "", "", "", "", ""]
        )
        np.testing.assert_array_equal(
            self.plt.get("C"),
            [
                "",
                "Test1",
                "Test1",
                "Test1",
                "Test1",
                "Test1",
                "Test1",
                "Test1",
                "Test1",
                "Test1",
                "Test2",
                "",
            ],
        )

    def test_name(self):
        self.assertEqual(self.plt.name, "Plate")

    def test_to_excel(self):
        self.plt.to_excel("test_plate_to_excel.xlsx")
        exist_plate = Path("test_plate_to_excel.xlsx").exists()
        self.assertTrue(exist_plate)

    def test_all_C(self):
        pl = BioPlate(6, 4)
        pl.set(2, [3, 4])
        np.testing.assert_array_equal(pl.get(2).tolist(), ["3", "4", "", ""])

    def test_multi_get(self):
        self.plt.set("A[2-3]", [4, 5])
        self.plt.set("4[D-F]", [6, 7, 8])
        R1 = self.plt.get("A[2-3]", "4[D-F]")
        self.assertEqual(R1, [["4", "5"], ["6", "7", "8"]])

    def test_merge(self):
        self.plt.set("A[2-3]", "Test")
        self.assertEqual(self.plt.get("A2"), "Test")
        self.plt.set("A[2-3]", ["_1", "_2"], merge=True)
        self.assertEqual(self.plt.get("A2"), "Test_1")
        self.assertEqual(self.plt.get("A3"), "Test_2")
        self.plt.set({"A2" : "_A", "A3" : "_B"}, merge=True)
        self.assertEqual(self.plt["A2"], "Test_1_A")
        self.assertEqual(self.plt["A3"], "Test_2_B")
        
    def test_set_get_item(self):
       p = BioPlate(12,8)
       p["A[4-6]"] = "bob"
       self.assertEqual(p["A6"], "bob")

    def test_partial_value(self):
        pl = BioPlate(12, 8)
        pl["A[5-9]"] = ["test", "test2", "test3"]
                
if __name__ == "__main__":
    unittest.main()
