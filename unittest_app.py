import os
import unittest
import json
import dropbox
import datetime
from shoeboxlocation import app


class TestIntegrations(unittest.TestCase):
    def setUp(self):
        """Set up the testclient and prepare testdata"""
        self.app = app.test_client()
        self.test_location = '{"lon": 12.0,"lat": 41.0}'
        self.test_location_int = '{"lon": 12,"lat": 41}'
        self.test_location_str = '{"lon": "12.0","lat": "41.0"}'
        self.test_no_json = '12.0,41.0'

    def test_post_status(self):
        """Test if the 'here' endpoint is handling incoming post requests."""
        res = self.app.post('/here', data=self.test_location)
        self.assertEqual(res.status_code, 200, msg=res.get_data(as_text=True))

    def test_post_float(self):
        """Test if the 'here' endpoint rejects post requests without float coordinates."""
        res = self.app.post('/here', data=self.test_location_int)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))
        res = self.app.post('/here', data=self.test_location_str)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_post_json(self):
        """Test if the 'here' endpoint rejects post requests without json post body."""
        res = self.app.post('/here', data=self.test_no_json)
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_post_empty(self):
        """Test if the 'here' endpoint rejects post requests without json post body."""
        res = self.app.post('/here')
        self.assertEqual(res.status_code, 400, msg=res.get_data(as_text=True))

    def test_get_status(self):
        """Test if the 'where' endpoint is handling incoming get requests."""
        res = self.app.get('/where')
        self.assertEqual(res.status_code, 200, msg=res.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
