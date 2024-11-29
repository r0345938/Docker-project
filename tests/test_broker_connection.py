import paho.mqtt.client as mqtt
import unittest
import time

BROKER = {
    'host': '172.16.0.72', 
    'port': 1883
}

class TestMQTTBrokerConnection(unittest.TestCase):

    def setUp(self):
        # Maak een nieuwe client
        self.client = mqtt.Client(client_id="test_client", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        print(f"on_connect called with rc={rc}")
        if rc == 0:
            print("Connected successfully to broker.")
            self.connected = True
        else:
            print(f"Connection failed with return code {rc}")
            self.connected = False

    def test_broker_connection(self):
        # Probeer verbinding te maken met de broker
        try:
            self.client.connect(BROKER['host'], BROKER['port'], 60)
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            self.fail("Exception raised during broker connection")

        # Start netwerkloop
        self.client.loop_start()
        print("Started MQTT loop")

        # Wacht maximaal 20 seconden op verbinding
        for _ in range(20):  # Wacht 20 seconden
            if self.connected:
                break
            time.sleep(1)

        self.client.loop_stop()
        print("Stopped MQTT loop")

        # Controleer of de verbinding succesvol was
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

    def tearDown(self):
        if self.connected:
            self.client.disconnect()


if __name__ == '__main__':
    unittest.main()
