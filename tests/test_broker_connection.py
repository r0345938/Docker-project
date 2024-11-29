import paho.mqtt.client as mqtt
import unittest
import time

BROKER = {
    'host': 'localhost', 
    'port': 1883
}

class TestMQTTBrokerConnection(unittest.TestCase):

    def setUp(self):
        # Make new client
        self.client = mqtt.Client(client_id="test_client", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.connected = False

        # Optional: add logging
        self.client.enable_logger()

    def on_connect(self, client, userdata, flags, rc):
        # controle
        if rc == 0:
            print("Connected successfully to broker.")
            self.connected = True
        elif rc == 1:
            print("Connection refused - incorrect protocol version.")
        elif rc == 2:
            print("Connection refused - invalid client identifier.")
        elif rc == 3:
            print("Connection refused - server unavailable.")
        elif rc == 4:
            print("Connection refused - bad username or password.")
        elif rc == 5:
            print("Connection refused - not authorised.")
        else:
            print(f"Failed to connect, unknown return code: {rc}")
        self.connected = False

    def test_broker_connection(self):
        # connect with broker
        try:
            self.client.connect(BROKER['host'], BROKER['port'], 60)
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            self.fail("Exception raised during broker connection")

        # Start loop to process network events
        self.client.loop_start()

        # Give more time te let the connection fail or be succesfull
        for _ in range(10):  # wait 10s to verify connectivity
            if self.connected:
                break
            time.sleep(1)

        # Stop the loop
        self.client.loop_stop()

        # Assert client make succesfull connection
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

    def tearDown(self):
        # Disconnect
        if self.connected:
            self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
