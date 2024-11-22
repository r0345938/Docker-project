import mysql.connector
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MySQL configuration
db_config = {
    'user': 'mqtt_user',
    'password': 'mqttpassword',
    'host': 'mysql-db',
    'database': 'mqtt_data',
}

def store_data_in_db(payload):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        insert_query = "INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)"
        cursor.execute(insert_query, (payload['temperature'], payload['pressure']))
        db.commit()
        logger.info(f"Data successfully inserted into database: {payload}")
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
    except Exception as e:
        logger.error(f"Unexpected error during database operation: {e}")
    finally:
        cursor.close()
        db.close()
        logger.info("MySQL connection closed.")