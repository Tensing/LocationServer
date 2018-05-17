import unittest
import json
import geojson
from shoeboxlocation import app


class TestIntegrations(unittest.TestCase):
    def setUp(self):
        """Set up the testclient and prepare testdata"""
        self.app = app.test_client()
        self.test_location = {"type": "Feature",
                              "properties": {
                                "name": "Shoebox"
                              },
                              "geometry": {
                                "type": "Point",
                                "coordinates": [
                                  4.5703125,
                                  51.83577752045248
                                ]
                              }}
        self.test_str = json.dumps(self.test_location)
        self.test_tuple = '4.5703125,51.83577752045248'


    def test_here_status(self):
        """Test if the 'here' endpoint is handling incoming post requests."""
        res = self.app.post('/here', data=self.test_str)
        self.assertEqual(res.status_code, 200, msg=res.get_data(as_text=True))

    def test_here_tuple(self):
        """Test if the 'here' endpoint rejects post requests with tuple of coordinates."""
        res = self.app.post('/here', data=self.test_tuple)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_here_empty(self):
        """Test if the 'here' endpoint rejects post requests without a post body."""
        res = self.app.post('/here')
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_where_status(self):
        """Test if the 'where' endpoint is handling incoming get requests."""
        res = self.app.get('/where')
        self.assertEqual(res.status_code, 200, msg=res.get_data(as_text=True))

    def test_where_coordinates(self):
        """Test if the 'where' endpoint is returning a json string with coordinates"""
        res = self.app.get('/where')
        try:
            data = geojson.loads(res.get_data(as_text=True))
            self.assertTrue(isinstance(data, geojson.feature.Feature),
                msg="Expected geojson feature, got {}".format(type(data)))
        except:
            raise

if __name__ == '__main__':
    unittest.main()
