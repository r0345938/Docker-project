import unittest
import mysql.connector

class TestMySQLDataAddition(unittest.TestCase):
    def setUp(self):
        # Making connection with MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="mqtt_user",
            password="mqttpassword",
            database="mqtt_data"
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # closing connection after every test
        self.cursor.close()
        self.conn.close()

    def test_data_addition(self):
        # Query to check if data is in MySQL database 
        self.cursor.execute("SELECT * FROM sensor_data WHERE temperature IS NOT NULL")
        result = self.cursor.fetchall()
        if len(result) > 0:
            print("Data found in MySQL sensor_data table.")
        
        # Check if data is in MySQL database
        self.assertGreater(len(result), 0, "No data found in MySQL sensor_data table.")

if __name__ == '__main__':
    unittest.main()
