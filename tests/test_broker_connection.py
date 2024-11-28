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
            self.connected = False

    def test_broker_connection(self):
        # Connect to the broker
        self.client.connect(BROKER['host'], BROKER['port'], 60)
        
        # Start the loop to process network events
        self.client.loop_start()
        
        # Geef meer tijd voor de verbinding of hercontroleer de connectiviteit.
        for _ in range(5):  # Tot 5 seconden wachten
            if self.connected:
                break
            time.sleep(1)
        
        self.client.loop_stop()

        # Assert client is connected
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

    def tearDown(self):
        self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
