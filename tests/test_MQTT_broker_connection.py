import paho.mqtt.client as mqtt
import unittest
import time
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BROKER1 = {
    'host': 'localhost',
    'port': 1883
}

BROKER2 = {
    'host': '172.16.0.72',
    'port': 1883
}

TOPIC = "sensor/data"
TEST_MESSAGE = '{"temperature": 25.0, "pressure": 1015.0}'

class TestMQTTBrokerConnection(unittest.TestCase):

    def setUp(self):
        # Set up a client to use in all tests.
        self.client = mqtt.Client(client_id="test_client", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.connected = False
        self.received_message = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info(f"Connected successfully to broker: {client._host}:{client._port}")
        else:
            logger.error(f"Failed to connect to broker with return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"Unexpected disconnection from broker: {client._host}:{client._port}")
        else:
            logger.info(f"Disconnected successfully from broker: {client._host}:{client._port}")
        self.connected = False

    def on_message(self, client, userdata, msg):
        self.received_message = msg.payload.decode()
        logger.info(f"Message received on topic {msg.topic}: {self.received_message}")

    def test_1_verify_broker_availability(self):
        # Connect to Broker 1 and verify availability
        logger.info("Attempting to connect to Broker 1...")
        self.client.connect(BROKER1['host'], BROKER1['port'], 60)
        self.client.loop_start()
        time.sleep(2)  # Give the client time to connect
        self.assertTrue(self.connected, "Broker 1 connection failed.")
        logger.info("Successfully connected to Broker 1.")

        # Ensure the client is only connected to broker 1
        self.assertEqual(self.client._host, BROKER1['host'], "Client is not connected to the expected broker.")
        logger.info("Client verified to be connected to the correct broker: Broker 1.")

    def test_2_disconnect_and_switch_to_another_broker(self):
        # Disconnect from Broker 1
        logger.info("Disconnecting from Broker 1...")
        self.client.disconnect()
        time.sleep(2)  # Give the client time to disconnect
        self.assertFalse(self.connected, "Failed to disconnect from broker 1.")
        logger.info("Successfully disconnected from Broker 1.")

        # Connect to Broker 2
        logger.info("Attempting to connect to Broker 2...")
        self.client.connect(BROKER2['host'], BROKER2['port'], 60)
        self.client.loop_start()
        time.sleep(2)  # Give the client time to connect
        self.assertTrue(self.connected, "Broker 2 connection failed.")
        self.assertEqual(self.client._host, BROKER2['host'], "Client is not connected to the expected broker.")
        logger.info("Successfully connected to Broker 2.")

    def test_3_verify_data_flow_to_selected_broker(self):
        # Publish a message to Broker 2 and verify reception
        logger.info("Connecting to Broker 2 for message verification...")
        self.client.connect(BROKER2['host'], BROKER2['port'], 60)
        self.client.loop_start()
        time.sleep(2)  # Give the client time to connect

        # Subscribe to topic
        logger.info(f"Subscribing to topic: {TOPIC}")
        self.client.subscribe(TOPIC)

        # Publish message
        logger.info(f"Publishing message to Broker 2 on topic {TOPIC}: {TEST_MESSAGE}")
        self.client.publish(TOPIC, TEST_MESSAGE)
        time.sleep(2)  # Allow message to be processed

        # Verify that the message was received correctly
        self.assertEqual(self.received_message, TEST_MESSAGE, "The received message did not match the published message.")
        logger.info("Message verification successful: Message received matches the published message.")

    def test_4_handle_broker_downtime(self):
        # Test client reconnection on broker shutdown
        logger.info("Connecting to Broker 2 to simulate broker downtime...")
        self.client.connect(BROKER2['host'], BROKER2['port'], 60)
        self.client.loop_start()
        time.sleep(2)  # Give the client time to connect

        # Simulate broker going down
        logger.info("Simulating broker downtime...")
        self.client.disconnect()
        time.sleep(2)
        self.assertFalse(self.connected, "Client should have disconnected when the broker went down.")
        logger.info("Broker downtime simulation successful: Client disconnected as expected.")

    def tearDown(self):
        logger.info("Tearing down client and stopping loop.")
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
