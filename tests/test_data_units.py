import mysql.connector
import unittest

class TestDataUnits(unittest.TestCase):

    def setUp(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="mqtt_user",
            password="mqttpassword",
            database="mqtt_data"
        )
        self.cursor = self.db_connection.cursor()

    def test_units(self):
        self.cursor.execute("SELECT temperature, pressure FROM sensor_data")
        for (temperature, pressure) in self.cursor:
            self.assertGreaterEqual(temperature, 20, "Temperature cannot be lower or equal as 20° Celsius.")
            self.assertGreaterEqual(pressure, 1000, "Pressure cannot be lower or equal as 1000 in hPa.")

    def tearDown(self):
        self.cursor.close()
        self.db_connection.close()

if __name__ == '__main__':
    unittest.main()

