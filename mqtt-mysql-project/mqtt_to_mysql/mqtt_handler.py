from paho.mqtt.client import Client
import logging
import json
from mqtt_to_mysql.mysql_handler import store_data_in_db

# Logger configuration
logger = logging.getLogger(__name__)

# MQTT configuration
BROKER_ADDRESS = "mqtt-broker"
PORT = 1883
TOPIC = "sensor/data"

def setup_mqtt_client():
    """
    Set up the MQTT client, including callbacks for connection and message reception.
    
    :return: Configured MQTT client.
    """
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER_ADDRESS, PORT, 60)
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        raise e

def on_connect(client, userdata, flags, rc):
    """
    Callback when the MQTT client connects to the broker.
    """
    if rc == 0:
        client.subscribe(TOPIC)
        logger.info(f"Connected to MQTT broker and subscribed to '{TOPIC}'")
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_message(client, userdata, msg):
    """
    Callback when a message is received from the broker.
    """
    logger.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    try:
        payload = json.loads(msg.payload.decode())
        logger.info(f"Decoded payload: {payload}")

        if 'temperature' in payload and 'pressure' in payload:
            store_data_in_db(payload)
        else:
            logger.warning("Unexpected JSON format. Required fields missing: 'temperature' and 'pressure'")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while processing the message: {e}")

def publish_message(client, topic, payload):
    """
    Publish a message to the given MQTT topic.
    
    :param client: MQTT client instance.
    :param topic: Topic to publish the message to.
    :param payload: The payload to publish.
    """
    try:
        payload_str = json.dumps(payload)
        client.publish(topic, payload_str)
        logger.info(f"Published test data to topic '{topic}': {payload_str}")
    except Exception as e:
        logger.error(f"Failed to publish message to topic '{topic}': {e}")
