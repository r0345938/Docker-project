from paho.mqtt.client import Client
import logging

# Logger configuratie
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("sensor/data")
        logger.info(f"Connected to MQTT broker and subscribed to 'sensor/data'")
    else:
        logger.error(f"Error connecting with MQTT-broker. Return code: {rc}")

def on_message(client, userdata, msg):
    logger.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

def setup_mqtt_client():
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("mqtt-broker", 1883, 60)
        return client
    except Exception as e:
        logger.error(f"Connection faillure with MQTT-broker: {e}")
        raise e
