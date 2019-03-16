import unittest
from BioPlate.core.index import Index


class TestIndex(unittest.TestCase):
   

    def test_str(self):
        self.assertEqual(Index("A2"), (1, 2)) 
        self.assertEqual(Index("B[2-6]"), (2, slice(2,7,1)))
        
    def test_int(self):
        self.assertEqual(Index(2), (2))
        self.assertEqual(Index((2, 1, 1)), (2,1,1))
        
    def test_slice(self):
        self.assertEqual(Index((slice(None, 3, 1), slice(None, 2, None))),(slice(None, 3, 1), slice(None, 2, None)))
 
if __name__ == "__main__":
    unittest.main() 