import unittest
import numpy

from BioPlate.array import BioPlateArray
from BioPlate import BioPlate


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
        pass

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.plate1 = BioPlateArray(12, 8)
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
            BioPlateArray.bioplatearray(2, ["test1"])
        self.assertEqual(BioPlateArray.bioplatearray([2, 3, 5]), [2, 3, 5])

    def test_get_columns_rows(self):
        self.assertEqual(BioPlateArray.get_columns_rows(["test1"]), (0,))
        with self.assertRaises(AttributeError):
            BioPlateArray.get_columns_rows(["test1"], ["test2"], [1, 2, 3])

    # def test__bio_plate_array(self):
    #     print(BioPlateArray._CACHE_BPA)
    #     self.assertEqual(self.plate1, BioPlateArray._CACHE_BPA[(12,8)])

    def test_get_plate_in_cache(self):
        with self.assertRaises(KeyError):
            BioPlateArray.get_columns_rows(BioPlateArray._get_plate_in_cache(245789))

    def test_get_stack_in_cache(self):
        with self.assertRaises(KeyError):
            BioPlateArray.get_columns_rows(BioPlateArray._get_stack_in_cache(245789))

    def test_merge_stack(self):
        id1 = id(self.stack1)
        id2 = id(self.stack2)
        self.assertEqual(
            BioPlateArray._merge_stack(id1, id2),
            [id(self.plate2), id(self.plate3), id(self.plate4), id(self.plate5)],
        )

    def test_add_plate_in_cache(self):
        BioPlateArray._add_plate_in_cache(12345, self.plate2)
        numpy.testing.assert_array_equal(self.plate2, BioPlateArray._PLATE_CACHE[12345])

    def test_get_list_id_of_stack(self):
        with self.assertRaises(ValueError):
            self.assertEqual(
                BioPlateArray._get_list_id_of_stack(self.plate2), [id(self.plate2)]
            )
        self.assertEqual(
            BioPlateArray._get_list_id_of_stack(self.stack1),
            [id(self.plate2), id(self.plate3)],
        )


if __name__ == "__main__":
    unittest.main()
