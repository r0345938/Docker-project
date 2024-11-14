import logging
import random
import time
import json
import paho.mqtt.client as mqtt

# Logger config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT config
BROKER_ADDRESS = "mqtt-broker"
PORT = 1883
TOPIC = "sensor/data"

def generate_test_data_continuously(interval=5):
    """
    Continuously generates test data and publishes it to the MQTT broker.
    
    :param interval: The number of seconds to wait between generating each new data row.
    
    """
    # Connect with MQTT broker
    client = mqtt.Client()
    try:
        logger.info(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{PORT}...")
        client.connect(BROKER_ADDRESS, PORT, 60)
        logger.info("Successfully connected to the MQTT broker.")
        
        while True:
            # Generate random temperature and pressure values
            temperature = round(random.uniform(20.0, 25.0), 2)
            pressure = round(random.uniform(1000.0, 1025.0), 2)
            payload = {
                "temperature": temperature,
                "pressure": pressure
            }
            payload_str = json.dumps(payload)

            # Publish the data to the MQTT topic
            client.publish(TOPIC, payload_str)
            logger.info(f"Published test data to topic '{TOPIC}': {payload_str}")

            # Wait for the interval before new data is generated
            time.sleep(interval)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

# If you want to run the script as a standalone program
if __name__ == "__main__":
    generate_test_data_continuously(interval=5)  # Generate data each 5s
