import unittest
from shoeboxlocation import here_is_shoebox, where_is_shoebox

class TestRequests(unittest.TestCase):
    def test_here_equals(self):
        request = {
            "data" : {
                "lon": 12,
                "lat": 34
            }
        }
        self.assertTrue(here_is_shoebox)


if __name__ == '__main__':
    unittest.main()
