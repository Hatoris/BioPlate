import unittest
import BioPlate.database.plate_db as pdb
import shutil
import os

class TestPlateDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
        pdb.add_plate(numWell=96,
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
        pdb.session.close_all()
        os.remove(os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', 'plate.db'))))

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.plate_list = pdb.get_plate(96)
        self.plate = pdb.get_plate(96)[0]

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        pass

    def test_get_plate(self):
        self.assertIsInstance(self.plate_list, list, "plate_db.get_plate don't return a list")
        #self.assertTrue(self.plate is pdb.get_plate(12, key="numColumns"))
        self.assertEquals('<plate N°1 : 96-12-8>', str(self.plate),
                          "plate_db.get_plate don't return the appropriate format")
        self.assertTrue(str(type(self.plate)) == "<class 'BioPlate.database.plate_db.PlateDB'>",
                        "plate_db.get_plate don't return the right class")

    def test_plate_class(self):
        self.assertEqual(self.plate.numWell, 96, "Error numWell association fail")
        self.assertEqual(self.plate.numColumns, 12, "Error numColumns association fail")
        self.assertEqual(self.plate.numRows, 8, "Error numRows association fail")
        self.assertEqual(self.plate.surfWell, 0.29, "Error numRows association fail")
        self.assertEqual(self.plate.maxVolWell, 200, "Error numRows association fail")
        self.assertEqual(self.plate.workVolWell, 200, "Error numRows association fail")
        self.assertEqual(self.plate.refURL, "https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
                         "Error refURL association fail")


if __name__ == '__main__':
    unittest.main()