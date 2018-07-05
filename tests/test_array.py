import unittest
import contextlib
#import mock
import numpy

from pathlib import Path, PurePath
from BioPlate.array import Array
from BioPlate import BioPlate
from BioPlate.database.plate_db import PlateDB


class TestBioPlateArray(unittest.TestCase):
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
        with contextlib.suppress(FileNotFoundError):
            Path(
                PurePath(
                    Path(__file__).parent.parent,
                    "BioPlate/database/DBFiles",
                    "plate.db",
                )
            ).unlink()

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.plate1 = Array(12, 8)
        self.plate2 = BioPlate(12, 8)
        self.plate3 = BioPlate(12, 8)
        self.plate4 = BioPlate(12, 8)
        self.plate5 = BioPlate(12, 8)
        self.stack1 = self.plate2 + self.plate3
        self.stack2 = self.plate4 + self.plate5

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test_bioplatearray(self):
        with self.assertRaises(ValueError):
            Array.bioplatearray(2, ["test1"])
        self.assertEqual(Array.bioplatearray([2, 3, 5]), [2, 3, 5])

    def test_get_columns_rows(self):
        self.assertEqual(Array.get_columns_rows(["test1"]), (0,))
        with self.assertRaises(AttributeError):
            Array.get_columns_rows(["test1"], ["test2"], [1, 2, 3])

    def test_get_plate_in_cache(self):
        with self.assertRaises(KeyError):
            Array.get_columns_rows(Array._get_plate_in_cache(245789))

    def test_get_stack_in_cache(self):
        with self.assertRaises(KeyError):
            Array.get_columns_rows(Array._get_stack_in_cache(245789))

    def test_merge_stack(self):
        id1 = id(self.stack1)
        id2 = id(self.stack2)
        self.assertEqual(
            Array._merge_stack(id1, id2),
            [id(self.plate2), id(self.plate3), id(self.plate4), id(self.plate5)],
        )
        with self.assertRaises(KeyError):
            Array._merge_stack(234345681, 3450834612)

    def test_add_plate_in_cache(self):
        Array._add_plate_in_cache(12345, self.plate2)
        numpy.testing.assert_array_equal(self.plate2, Array._PLATE_CACHE[12345])

    def test_get_list_id_of_stack(self):
        with self.assertRaises(ValueError):
            self.assertEqual(
                Array._get_list_id_of_stack(self.plate2), [id(self.plate2)]
            )
        self.assertEqual(
            Array._get_list_id_of_stack(self.stack1),
            [id(self.plate2), id(self.plate3)],
        )

    def test_attributeError(self):
        with self.assertRaises(AttributeError):
            Array({"1" : "a"})

    def test_get_plate_in_stack(self):
        with self.assertRaises(KeyError):
            Array._get_plate_in_stack(1234567890, 1)
        with self.assertRaises(IndexError):
            Array._get_plate_in_stack(id(self.stack1), 10)
            
            

if __name__ == "__main__":
    unittest.main()
