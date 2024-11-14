import mysql.connector
import logging

# Logger config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db_config = {
    'user': 'mqtt_user',
    'password': 'mqttpassword',
    'host': 'mysql-db',
    'database': 'mqtt_data'
}

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(**db_config)
        logger.info("Connection success MySQL.")
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Error connection MySQL: {err}")
        return None

def insert_sensor_data(temperature, pressure):
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            insert_query = "INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)"
            cursor.execute(insert_query, (temperature, pressure))
            connection.commit()
            logger.info(f"Data stored in database: temperature={temperature}, pressure={pressure}")
        except mysql.connector.Error as err:
            logger.error(f"Error inserting data
: {err}")
        finally:
            cursor.close()
            connection.close()
