import shoeboxlocation
from unittest import TestCase

wclass TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_thing(self):
        response = self.app.post('/where', json='{"lon": 12,"lat": 35}')
        assert <make your assertion here>
