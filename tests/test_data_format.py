import mysql.connector
import unittest

class InvalidDataError(Exception):
    """Custom exception for invalid data."""
    pass

class TestDataFormat(unittest.TestCase):

    def setUp(self):
        print("Setting up test environment")  # Debugging statement
        # Make connection with database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="mqtt_user",
            password="mqttpassword",
            database="mqtt_data"
        )
        self.cursor = self.db_connection.cursor()

        # Making table (if required)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                temperature FLOAT NOT NULL,
                pressure FLOAT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Define correct and invalid data
        self.correct_data = [
            (22.5, 1013.25),
            (19.25, 1012.02),
            (25.0, 1015.00),
        ]
        self.invalid_data = [
            ("invalid", 1013.25),  # Temperature is a string
            (22.5, "invalid"),  # Pressure is a string
            (None, 1013.25),  # Temperature is None
            (22.5, None),  # Pressure is None
        ]

        # Delete all previous data (so tests start clean)
        self.cursor.execute("DELETE FROM sensor_data")
        self.db_connection.commit()

    def validate_data(self, data):
        """Validates data before inserting into the database."""
        for temperature, pressure in data:
            if not isinstance(temperature, (int, float)) or temperature is None:
                raise InvalidDataError(f"Invalid temperature value: {temperature}")
            if not isinstance(pressure, (int, float)) or pressure is None:
                raise InvalidDataError(f"Invalid pressure value: {pressure}")

    def test_correct_data(self):
        print("Running test_correct_data")  # Debugging statement

        # Validate correct data
        try:
            self.validate_data(self.correct_data)
        except InvalidDataError as e:
            self.fail(f"Validation failed for correct data: {e}")

        # adding correct data
        self.cursor.executemany(
            "INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)",
            self.correct_data
        )
        self.db_connection.commit()

        # Check whether the data is correct in the database
        self.cursor.execute("SELECT temperature, pressure FROM sensor_data")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), len(self.correct_data), "Not all correct data was inserted.")
        for (temperature, pressure) in rows:
            self.assertIsInstance(temperature, float, "Temperature is not in float format.")
            self.assertIsInstance(pressure, float, "Pressure is not in float format.")

    def test_invalid_data(self):
        print("Running test_invalid_data")  # Debugging statement

        # Try to validate incorrect data and check if it causes an error
        with self.assertRaises(InvalidDataError):
            self.validate_data(self.invalid_data)

        # Check that no incorrect data enters the database
        for temp, pres in self.invalid_data:
            try:
                self.cursor.execute(
                    "INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)",
                    (temp, pres)
                )
            except mysql.connector.errors.DatabaseError as db_error:
                print(f"Database rejected invalid data: {temp}, {pres} -> {db_error}")
            else:
                self.fail(f"Invalid data was inserted into the database: {temp}, {pres}")
            self.db_connection.rollback()  # Make sure the error does not impact the table

    def print_database_contents(self):
        """Print the current contents of the sensor_data table."""
        self.cursor.execute("SELECT * FROM sensor_data")
        rows = self.cursor.fetchall()
        if rows:
            print("\nCurrent contents of sensor_data:")
            for row in rows:
                print(row)
        else:
            print("\nThe sensor_data table is empty.")

    def tearDown(self):
        print("Tearing down test environment")  # Debugging statement
        # Remove all data from the table after each test
        self.cursor.execute("DELETE FROM sensor_data")
        self.db_connection.commit()

        # close cursor and databaseconnection
        self.cursor.close()
        self.db_connection.close()


if __name__ == '__main__':
    unittest.main()
