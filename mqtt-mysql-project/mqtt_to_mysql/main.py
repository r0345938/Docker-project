import logging
import time
import threading
from mqtt_handler import setup_mqtt_client


# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_mqtt_client():
    try:
        logger.info("Starting the MQTT client...")
        client = setup_mqtt_client()
        client.loop_start()  # Start the MQTT client in a separate thread so that the script does not stop
        return client
    except Exception as e:
        logger.error(f"Error occurred while setting up MQTT client: {e}")
        raise e

def start_generating_test_data():
    logger.info("Starting continuous data generation via MQTT...")
    testdata_thread = threading.Thread(target=generate_test_data_continuously, args=(5,), daemon=True)
    testdata_thread.start()

if __name__ == "__main__":
    # Start the MQTT client
    client = start_mqtt_client()

    # Wait a few seconds to ensure MySQL is ready
    time.sleep(15)

    # Start continuous data generation
    start_generating_test_data()

    # Keep the container running
    logger.info("MQTT client is now running. Keeping the container alive...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
