import unittest
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.database.plate_db import PlateDB
from BioPlate import BioPlate
from pathlib import Path, PurePath
import contextlib
import numpy as np
import datetime


class TestPlateDB(unittest.TestCase):
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
        v = {
            "A[2,8]": "VC",
            "H[2,8]": "MS",
            "1-4[B,G]": ["MLR", "NT", "1.1", "1.2"],
            "E-G[8,10]": ["Val1", "Val2", "Val3"],
        }
        cls.plt = BioPlate({"id": 1}, db_name="test_plate.db")
        cls.plt.set(v)
        cls.phi = PlateHist(db_name="test_plate_historic.db")
        cls.phi.add_hplate(
            Plate_id=1,
            numWell=96,
            plate_name="First plate to test",
            plate_array=cls.plt,
        )
        dt = datetime.datetime.now()
        cls.date = datetime.date(dt.year, dt.month, dt.day)

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

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.plate_list = self.phi.get_hplate(numWell=96)
        self.plate = self.plate_list[0]

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test_get_hplate(self):
        self.assertIsInstance(
            self.plate_list, list, "plate_db.get_plate don't return a list"
        )
        self.assertEqual(
            f"<plate N°1: First plate to test, 96 wells, {self.phi.date_now}>",
            str(self.plate),
            "plate_db.get_plate don't return the appropriate format",
        )
        self.assertTrue(
            str(type(self.plate))
            == "<class 'BioPlate.database.plate_historic_db.PlateHist.PlateHistoric'>",
            f"plate_db.get_plate don't return the right class : {str(type(self.plate))}",
        )

    def test_plate_class(self):
        self.assertEqual(self.plate.numWell, 96, "Error numWell association fail")
        self.assertEqual(
            self.plate.plate_name,
            "First plate to test",
            "Error numColumns association fail",
        )
        np.testing.assert_array_equal(self.plate.plate_array, self.plt)

    def test_add_hplate(self):
        add_plate_1 = self.pdb.add_plate(
            numWell=6,
            numColumns=3,
            numRows=2,
            surfWell=9.5,
            maxVolWell=2000,
            workVolWell=2000,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        p6 = self.pdb.get_one_plate(6)
        Plate6 = BioPlate({"numWell": 6}, db_name="test_plate.db")
        add_hplate_1 = self.phi.add_hplate(
            Plate_id=2, numWell=6, plate_name="second plate", plate_array=Plate6
        )
        add_hplate_2 = self.phi.add_hplate(
            Plate_id=2, numWell=6, plate_name="second plate", plate_array=Plate6
        )
        self.assertEqual(
            add_hplate_1,
            "BioPlatePlate second plate with 6 wells was successfully added to database test_plate_historic.db",
        )
        self.assertEqual(add_hplate_2, 2)
        self.assertEqual(
            f"<plate N°2: second plate, 6 wells, {self.phi.date_now}>",
            str(self.phi.get_one_hplate(6)),
        )
        self.assertEqual(6, self.phi.get_hplate(numWell=6)[0].numWell)

    def test_delete_hplate(self):
        self.assertEqual(self.phi.delete_hplate(6), "plate with 6 numWell deleted")
        self.assertEqual(self.phi.get_hplate(numWell=6), [])

    def test_repr(self):
        Pl = self.phi.get_one(1, key="id")
        self.assertEqual(repr(Pl), f"<plate N°1: First plate to test, 96 wells, {self.date}>")

    def test_get_all(self):
        self.assertEqual(str(self.phi.get_all_hplate()), f"[<plate N°1: First plate to test, 96 wells, {self.date}>]")
        
    def test_stack(self):
       pl1 = BioPlate(12, 8)
       pl2 = BioPlate(12, 8)
       pl1.set("A2", "bob")
       self.phi.add_hplate(
            Plate_id=2, numWell=96, plate_name="stack", plate_array=[pl1, pl2]
        )
       Pl = self.phi.get_one(2, key="id").plate
       self.assertEqual(Pl.name, "BioPlateStack")
       self.assertEqual(Pl.get(0, "A2"), "bob")
      
if __name__ == "__main__":
    unittest.main()
