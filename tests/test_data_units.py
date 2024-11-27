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

        # Insert testdata
        insert_query = "INSERT INTO sensor_data (temperature, pressure, timestamp) VALUES (%s, %s, NOW())"
        test_data = [
            (20.0, 1020.0),  
            (25.0, 1000.0), 
            (15.0, 999.0) # Test faillure
        ]
        self.cursor.executemany(insert_query, test_data)
        self.db_connection.commit()  # Commit data to database

    def test_units(self):
        # excecute query to collect data
        self.cursor.execute("SELECT temperature, pressure FROM sensor_data")
        result = self.cursor.fetchall()  # Collecting values
        print(result)  # Debug to check the value of the data

        # Assertion to check values are correct
        for (temperature, pressure) in result:
            self.assertGreaterEqual(temperature, 20, "Temperature cannot be lower than 20° Celsius.")
            self.assertGreaterEqual(pressure, 1000, "Pressure cannot be lower than 1000 hPa.")

    def tearDown(self):
        # close cursor and connection
        self.cursor.close()
        self.db_connection.close()

if __name__ == '__main__':
    unittest.main()
