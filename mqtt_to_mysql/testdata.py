import logging
import random
import mysql.connector
import time

# Logger configuratie
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuratie
db_config = {
    'user': 'mqtt_user',
    'password': 'mqttpassword',
    'host': 'mysql-db',
    'database': 'mqtt_data',
}

def generate_test_data_continuously(interval=5):
    """
    Continuously generates test data and stores it in the MySQL database.
    
    :param interval: The number of seconds to wait between generating each new data row.
    """
    try:
        logger.info(f"Connecting to MySQL to start generating continuous test data...")
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        while True:
            # Generate random temperature- and pressurevalues
            temperature = round(random.uniform(20.0, 25.0), 2)
            pressure = round(random.uniform(1000.0, 1025.0), 2)
            insert_query = "INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)"
            cursor.execute(insert_query, (temperature, pressure))
            db.commit()
            logger.info(f"Inserted test data: temperature={temperature}, pressure={pressure}")

            # Wait for the interval before new data is generated
            time.sleep(interval)

    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        cursor.close()
        db.close()
        logger.info("Stopped generating test data. MySQL connection closed.")

# run the script as a standalone program
if __name__ == "__main__":
    generate_test_data_continuously(interval=5)  # Generate data each 5s
