import mysql.connector
import unittest

class TestDataFormat(unittest.TestCase):

    def setUp(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            port= 3306,
            user="mqtt_user",
            password="mqttpassword",
            database="mqtt_data"
        )
        self.cursor = self.db_connection.cursor()

    def test_data_format(self):
        # Check if there are float values in temperature and pressure in MySQL-database
        self.cursor.execute("SELECT temperature, pressure FROM sensor_data")
        for (temperature, pressure) in self.cursor:
            self.assertIsInstance(temperature, float, "Temperature is not in float format.")
            self.assertIsInstance(pressure, float, "Pressure is not in float format.")

    def test_no_strings_in_columns(self):
        # Check if there are no string values in temperature and pressure in MySQL-database
        self.cursor.execute("SELECT temperature, pressure FROM sensor_data")
        for (temperature, pressure) in self.cursor:
            self.assertNotIsInstance(temperature, str, "Temperature should not be a string.")
            self.assertNotIsInstance(pressure, str, "Pressure should not be a string.")

    def tearDown(self):
        self.cursor.close()
        self.db_connection.close()

if __name__ == '__main__':
    unittest.main()
