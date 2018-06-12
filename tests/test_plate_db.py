import unittest
from BioPlate.database.plate_db import PlateDB
import contextlib
from pathlib import Path, PurePath
from sqlalchemy import exc
import sqlite3


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

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.plate_list = self.pdb.get_plate(numWell=96)
        self.plate = self.plate_list[0]

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path("test_plate.db").absolute().unlink()

    def test_get_plate(self):
        self.assertIsInstance(
            self.plate_list, list, "plate_db.get_plate don't return a list"
        )
        self.assertEqual(
            "<plate N°1 : 96-12-8>",
            str(self.plate),
            "plate_db.get_plate don't return the appropriate format",
        )
        self.assertTrue(
            str(type(self.plate))
            == "<class 'BioPlate.database.plate_db.PlateDB.PlateDatabase'>",
            f"plate_db.get_plate don't return the right class : {str(type(self.plate))}",
        )

    def test_plate_class(self):
        self.assertEqual(self.plate.numWell, 96, "Error numWell association fail")
        self.assertEqual(self.plate.numColumns, 12, "Error numColumns association fail")
        self.assertEqual(self.plate.numRows, 8, "Error numRows association fail")
        self.assertEqual(self.plate.surfWell, 0.29, "Error numRows association fail")
        self.assertEqual(self.plate.maxVolWell, 200, "Error numRows association fail")
        self.assertEqual(self.plate.workVolWell, 200, "Error numRows association fail")
        self.assertEqual(
            self.plate.refURL,
            "https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
            "Error refURL association fail",
        )

    def test_add_plate(self):
        add_plate_1 = self.pdb.add_plate(
            numWell=6,
            numColumns=3,
            numRows=2,
            surfWell=9.5,
            maxVolWell=2000,
            workVolWell=2000,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        self.assertEqual(add_plate_1, "plate with 6 added to the database")
        add_plate_2 = self.pdb.add_plate(
            numWell=6,
            numColumns=3,
            numRows=2,
            surfWell=9.5,
            maxVolWell=2000,
            workVolWell=2000,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        self.assertEqual(add_plate_2, None)
        self.assertEqual("<plate N°2 : 6-3-2>", str(self.pdb.get_plate(numWell=6)[0]))
        self.assertEqual(6, self.pdb.get_plate(numWell=6)[0].numWell)

    def test_delete_plate(self):
        self.pdb.add_plate(
            numWell=24,
            numColumns=6,
            numRows=4,
            surfWell=0.33,
            maxVolWell=400,
            workVolWell=400,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        self.assertEqual(self.pdb.delete_plate(24), "plate with 24 numWell deleted")
        self.assertEqual(self.pdb.get_plate(numWell=24), [])

    def test_update_plate(self):
        self.pdb.add_plate(
            numWell=24,
            numColumns=6,
            numRows=4,
            surfWell=0.33,
            maxVolWell=400,
            workVolWell=400,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        plate_24 = self.pdb.get_plate(numWell=24)[0]
        self.assertEqual(plate_24.name, None)
        self.assertEqual(plate_24.surfWell, 0.33)
        update = {"name": "24_well", "surfWell": 0.3}
        self.assertEqual(
            self.pdb.update_plate(update, 24), "plate with 24 numWell updated"
        )
        plate_24_update = self.pdb.get_plate(numWell=24)[0]
        self.assertEqual(plate_24_update.name, "24_well")
        self.assertEqual(plate_24_update.surfWell, 0.3)
        self.pdb.add_plate(
            numWell=24,
            numColumns=6,
            numRows=4,
            surfWell=0.33,
            maxVolWell=400,
            workVolWell=400,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        update = {"name": "24_well", "surfWell": 0.3}
        self.assertEqual(
            self.pdb.update_plate(update, 24),
            "Use a more specific key to update the object",
        )

    def test_get_one(self):
        with self.assertRaises(ValueError):
            self.pdb.get_one(12)
            self.pdb.get("a")
        self.pdb.add_plate(
            numWell=96,
            numColumns=12,
            numRows=8,
            surfWell=0.29,
            maxVolWell=200,
            workVolWell=200,
            refURL="https://csmedi2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )

        self.assertEqual(
            self.pdb.get_one(96, key="numWell"),
            "Use a more specific key to get one object",
        )

    def test_get_error(self):
        with self.assertRaises(exc.InvalidRequestError):
            self.pdb.get(numWel=6)

    def test_get_all_error(self):
        pdbt = PlateDB(db_name="tt_plate.db")
        pdbt.add_plate(
            numWell=96,
            numColumns=12,
            numRows=8,
            surfWell=0.29,
            maxVolWell=200,
            workVolWell=200,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        Path(
            PurePath(
                Path(__file__).parent.parent, "BioPlate/database/DBFiles", "tt_plate.db"
            )
        ).unlink()

        # with self.assertRaises(exc.SQLAlchemyError):
        pdbt.get_all()

    def test_delete(self):
        self.pdb.add_plate(
            numWell=6,
            numColumns=3,
            numRows=6,
            surfWell=0.29,
            maxVolWell=200,
            workVolWell=200,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )
        self.pdb.add_plate(
            numWell=6,
            numColumns=3,
            numRows=6,
            surfWell=0.29,
            maxVolWell=200,
            workVolWell=200,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_aras.pdf",
        )
        with self.assertRaises(ValueError):
            self.pdb.delete(24)
        self.assertEqual(
            self.pdb.delete(6, key="numWell"),
            "Use a more specific key to delete the object",
        )

    def test_update(self):
        with self.assertRaises(ValueError):
            self.pdb.update({"numWell": 15}, 12)


if __name__ == "__main__":
    unittest.main()
