"""
Unit tests for server module

When run as a script, this module invokes several procedures that
test the various requests of the server module.
"""
import unittest
import requests
url1 = "http://localhost:5000/vehicles/1234"
url2 = "http://localhost:5000/vehicles/1235"

class TestSmartCarAPI(unittest.TestCase):

    def test_info(self):
        # Tests for vehicle 1234
        r = requests.get(url1).json()
        self.assertEqual(r["color"], "Metallic Silver")
        self.assertEqual(r["doorCount"], 4)
        self.assertEqual(r["driveTrain"], "v8")
        self.assertEqual(r["vin"], "123123412412")

        # Tests for vehicle 1235
        s = requests.get(url2).json()
        self.assertEqual(s["color"], "Forest Green")
        self.assertEqual(s["doorCount"], 4)
        self.assertEqual(s["driveTrain"], "electric")
        self.assertEqual(s["vin"], "1235AZ91XP")


    def test_security(self):
        # Tests for vehicle 1234
        r = requests.get(url1 + "/doors").json()
        for door in r:
            self.assertEqual(type(door["location"]), unicode)
            self.assertEqual(type(door["locked"]), bool)

        # Tests for vehicle 1235
        s = requests.get(url2 + "/doors").json()
        for door in s:
            self.assertEqual(type(door["location"]), unicode)
            self.assertEqual(type(door["locked"]), bool)


    def test_fuel(self):
        # Tests for vehicle 1234
        r = requests.get(url1 + "/fuel").json()
        self.assertEqual(type(r["percent"]), float)
        self.assertTrue(r["percent"]>=0.0 and r["percent"]<=100.0)

        # Tests for vehicle 1235
        s = requests.get(url2 + "/fuel").json()
        self.assertEqual(type(s["percent"]), float)
        self.assertTrue(s["percent"]>=0.0 and s["percent"]<=100.0)


    def test_battery(self):
        # Tests for vehicle 1234
        r = requests.get(url1 + "/battery").json()
        self.assertEqual(type(r["percent"]), float)
        self.assertTrue(r["percent"]>=0.0 and r["percent"]<=100.0)

        # Tests for vehicle 1235
        s = requests.get(url2 + "/battery").json()
        self.assertEqual(type(s["percent"]), float)
        self.assertTrue(s["percent"]>=0.0 and s["percent"]<=100.0)


    def test_engine(self):
        start = {"action": "START"}
        stop = {"action": "STOP"}
        # Tests for vehicle 1234
        r = requests.post(url1 + "/engine", json = start).json()
        self.assertTrue(r["status"]=="success" or r["status"]=="failure")
        r = requests.post(url1 + "/engine", json = stop).json()
        self.assertTrue(r["status"]=="success" or r["status"]=="failure")

        # Tests for vehicle 1235
        s = requests.post(url2 + "/engine", json = start).json()
        self.assertTrue(s["status"]=="success" or s["status"]=="failure")
        s = requests.post(url2 + "/engine", json = stop).json()
        self.assertTrue(s["status"]=="success" or s["status"]=="failure")


if __name__ == '__main__':
    unittest.main()
