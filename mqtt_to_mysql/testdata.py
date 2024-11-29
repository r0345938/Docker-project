import logging
import random
import time
import string
from mqtt_to_mysql.mqtt_handler import setup_mqtt_client, publish_message

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT configuration
TOPIC = "sensor/data"

def generate_test_data_continuously(interval=5):
    """
    Continuously generates test data and publishes it to the MQTT broker.

    :param interval: The number of seconds to wait between generating each new data row.
    """
 # Set up MQTT client
    #client = setup_mqtt_client() # USE ONLY FOR TESTDATA + IN COMMENT FOR DAMIAN'S DATA
    
    try:
        while True:
            # Generate random temperature and pressure values
            temperature = round(random.uniform(20.0, 25.0), 2)
            pressure = round(random.uniform(1000.0, 1025.0), 2)

            # TESTING Generate random temperature and pressure values (NO FLOAT)
            #temperature =  random.randint(20, 25)
            #pressure = random.randint(1000, 1025)

            # TESTING Generate random strings for temperature and pressure
            #temperature = ''.join(random.choice(string.ascii_letters) for i in range(5))
            #pressure = ''.join(random.choice(string.ascii_letters) for i in range(4))

            payload = {
                "temperature": temperature,
                "pressure": pressure
            }

            # Publish the data to the MQTT topic using the mqtt_handler
            publish_message(client, TOPIC, payload)

            # Wait for the interval before generating new data
            time.sleep(interval)

    except Exception as e:
        logger.error(f"Unexpected error during data generation: {e}")

# If you want to run the script as a standalone program
if __name__ == "__main__":
    generate_test_data_continuously(interval=5)  # Generate data each 5 seconds