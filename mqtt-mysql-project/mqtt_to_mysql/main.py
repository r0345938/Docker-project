from mqtt_handler import setup_mqtt_client
from testdata import generate_test_data_continuously
import logging
import time
import threading

# Logger configuratie
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Start de MQTT client
    try:
        logger.info("Starting the MQTT client...")
        client = setup_mqtt_client()
        client.loop_start()  # Start de MQTT client in een aparte thread zodat het script niet stopt
    except Exception as e:
        logger.error(f"Error occurred while setting up MQTT client: {e}")

    # Wacht een paar seconden voordat we de MySQL-server benaderen
    time.sleep(30)  # Wacht 30 seconden om er zeker van te zijn dat MySQL gereed is

    # Start het genereren van continue testdata in een aparte thread
    logger.info("Starting continuous data generation...")
    testdata_thread = threading.Thread(target=generate_test_data_continuously, args=(5,), daemon=True)
    testdata_thread.start()

    # Houd de container draaiende
    logger.info("MQTT client is now running. Keeping the container alive...")
    while True:
        time.sleep(1)
