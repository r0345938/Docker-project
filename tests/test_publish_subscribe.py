import paho.mqtt.client as mqtt
import unittest
import time

BROKER = {
    'host': '172.16.0.72',
    'port': 1883
}
TOPIC = "sensor/data"
TEST_MESSAGE = '{"temperature": 20.01, "pressure": 1024.99}'

class TestMQTTPublishSubscribe(unittest.TestCase):

    def setUp(self):
        # Create a new MQTT client instance for testing
        self.client = mqtt.Client(client_id="test_publisher_subscriber", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.connected = False
        self.received_message = None

    # Callback for when the client connects to the broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected successfully to broker.")
            client.subscribe(TOPIC)
        else:
            print("Connection failed with code:", rc)

    # Callback for when a message is received from the broker
    def on_message(self, client, userdata, msg):
        print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
        self.received_message = msg.payload.decode()

    # Test method to publish a message and check if it's received
    def test_publish_and_subscribe(self):
        # Connect to broker
        self.client.connect(BROKER['host'], BROKER['port'], 60)
        self.client.loop_start()  # Start loop to process received messages in background

        # Wait until connected
        time.sleep(2)
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

        # Publish test message
        self.client.publish(TOPIC, TEST_MESSAGE)

        # Wait for message to be received
        time.sleep(2)
        self.assertEqual(self.received_message, TEST_MESSAGE, "The received message did not match the published message.")

        # Stop loop
        self.client.loop_stop()

    def tearDown(self):
        # Disconnect the client after the test is done
        self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
