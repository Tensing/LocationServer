import unittest
import json
from shoeboxlocation import app


class TestIntegrations(unittest.TestCase):
    def setUp(self):
        """Set up the testclient and prepare testdata"""
        self.app = app.test_client()
        self.test_location = '{"lon": 12.0,"lat": 41.0}'
        self.test_location_obj = {"lon": 12.0,"lat": 41.0}
        self.test_location_int = '{"lon": 12,"lat": 41}'
        self.test_location_str = '{"lon": "12.0","lat": "41.0"}'
        self.test_tuple = '12.0,41.0'

    def test_here_status(self):
        """Test if the 'here' endpoint is handling incoming post requests."""
        res = self.app.post('/here', data=self.test_location)
        self.assertEqual(res.status_code, 200, msg=res.get_data(as_text=True))

    def test_here_float(self):
        """Test if the 'here' endpoint rejects post requests without float coordinates."""
        res = self.app.post('/here', data=self.test_location_int)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))
        res = self.app.post('/here', data=self.test_location_str)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_here_tuple(self):
        """Test if the 'here' endpoint rejects post requests with tuple of coordinates."""
        res = self.app.post('/here', data=self.test_tuple)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_here_empty(self):
        """Test if the 'here' endpoint rejects post requests without a post body."""
        res = self.app.post('/here')
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_here_object(self):
        """Test if the 'here' endpoint rejects post requests without object data."""
        res = self.app.post('/here', data=self.test_location_obj)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_where_status(self):
        """Test if the 'where' endpoint is handling incoming get requests."""
        res = self.app.get('/where')
        self.assertEqual(res.status_code, 200, msg=res.get_data(as_text=True))

    def test_where_coordinates(self):
        """Test if the 'where' endpoint is returning a json string with coordinates"""
        res = self.app.get('/where')
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue("lat" in data.keys(), msg="No 'lat' coordinate found")
        self.assertTrue("lon" in data.keys(), msg="No 'lon' coordinate found")

if __name__ == '__main__':
    unittest.main()
