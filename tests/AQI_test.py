from unittest import TestCase

from AQI import AQIMonitor

class AQI_test(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_geocode(self):
        aqi = AQIMonitor()
        seattle_coord = (47.6061, -122.3328)
        api_response_seattle = aqi.geocode("Seattle", "Washington", "United States")
        self.assertAlmostEqual(round(seattle_coord[0], 1), round(api_response_seattle[0], 1), msg="Wrong Response for Longitude")
        self.assertAlmostEqual(round(seattle_coord[1], 1), round(api_response_seattle[1], 1), msg="Wrong Response for Latitude")

    def test_unix_timestamp(self):
        aqi = AQIMonitor()
        self.assertEqual(1731146400, aqi.to_unix_timestamp(11, 9, 2024, 2, 0), msg="Wrong Response for UNIX Timestamp")