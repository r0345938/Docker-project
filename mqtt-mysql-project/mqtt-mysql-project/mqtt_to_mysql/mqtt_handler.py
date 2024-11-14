from paho.mqtt.client import Client
import logging
import json
import mysql.connector

# Logger config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MySQL config
db_config = {
    'user': 'mqtt_user',
    'password': 'mqttpassword',
    'host': 'mysql-db',
    'database': 'mqtt_data',
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("sensor/data")
        logger.info("Connected to MQTT broker and subscribed to 'sensor/data'")
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_message(client, userdata, msg):
    logger.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    try:
        payload = json.loads(msg.payload.decode())
        logger.info(f"Decoded payload: {payload}")

        if 'temperature' in payload and 'pressure' in payload:
            # Connect with MySQL
            try:
                db = mysql.connector.connect(**db_config)
                cursor = db.cursor()
                
                # Add data into database
                insert_query = "INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)"
                cursor.execute(insert_query, (payload['temperature'], payload['pressure']))
                db.commit()
                logger.info(f"Data successfully inserted into database: {payload}")
                
            except mysql.connector.Error as err:
                logger.error(f"Database error: {err}")
            except Exception as e:
                logger.error(f"Unexpected error during database operation: {e}")
            finally:
                if cursor:
                    cursor.close()
                if db:
                    db.close()
                logger.info("MySQL connection closed.")
        else:
            logger.warning("Unexpected JSON format. Required fields missing: 'temperature' and 'pressure'")
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while processing the message: {e}")

def setup_mqtt_client():
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("mqtt-broker", 1883, 60)
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        raise e
