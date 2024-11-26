import paho.mqtt.client as mqtt
import unittest
import time

BROKER = {
    'host': 'localhost',
    'port': 1883
}

class TestMQTTBrokerConnection(unittest.TestCase):

    def setUp(self):
        # Create a new client instance 
        self.client = mqtt.Client(client_id="test_client", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully to broker.")
            self.connected = True
        else:
            print(f"Failed to connect, return code {rc}")

    def test_broker_connection(self):
        # Connect to the broker
        self.client.connect(BROKER['host'], BROKER['port'], 60)
        
        # Start the loop to process network events, and allow some time for connection
        self.client.loop_start()
        time.sleep(2)  # Give client time to make connection
        self.client.loop_stop()

        # Assert client is connected
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

    def tearDown(self):
        self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
