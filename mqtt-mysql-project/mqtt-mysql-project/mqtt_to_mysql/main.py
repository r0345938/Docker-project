from mqtt_handler import setup_mqtt_client
from testdata import generate_test_data_continuously
import logging
import time
import threading

# Logger configuratie
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Start MQTT client
    try:
        logger.info("Starting the MQTT client...")
        client = setup_mqtt_client()
        client.loop_start()  # Start the MQTT client in a separate thread so that the script does not stop 
    except Exception as e:
        logger.error(f"Error occurred while setting up MQTT client: {e}")

    # Please wait 30 seconds before we access the MySQL server
    time.sleep(30)  

    # Start generating continuous test data in a separate thread and send it via MQTT
    logger.info("Starting continuous data generation via MQTT...")
    testdata_thread = threading.Thread(target=generate_test_data_continuously, args=(5,), daemon=True)
    testdata_thread.start()

    # Keep the container running
    logger.info("MQTT client is now running. Keeping the container alive...")
    while True:
        time.sleep(1)
