import unittest
from BioPlate.core.index import Index


class TestIndex(unittest.TestCase):
   

    def test_str(self):
        self.assertEqual(Index("A2"), ("W", (1, 2))) 
        self.assertEqual(Index("B[2-6]"), ("R", (2, slice(2,7,1))))
        
    def test_int(self):
        self.assertEqual(Index(2), (None, (2,)))
        self.assertEqual(Index((2, 1, 1)), (None, (2,1,1)))
        
    def test_slice(self):
        self.assertEqual(Index((slice(None, 3, 1), slice(None, 2, None))),(None, (slice(None, 3, 1), slice(None, 2, None))))
        
    def test_int_str(self):
        self.assertEqual(Index((1, "1")), ("C", (1, slice(1, None, None), 1)))
 
    def test_row_str(self):
        self.assertEqual(Index("B"), ("R", (2, slice(1, None, None))))
 
if __name__ == "__main__":
    unittest.main() 