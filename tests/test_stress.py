import paho.mqtt.client as mqtt
import unittest
import time
import timeit

BROKER = {'host': '172.16.0.72', 'port': 1883}
TOPIC = "sensor/data"

class TestMQTTStress(unittest.TestCase):

    def setUp(self):
        self.client = mqtt.Client(client_id="stress_test_client", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.connected = False
        self.message_count = 0
        self.total_messages = 150

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected successfully to broker.")
            client.subscribe(TOPIC)
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        self.message_count += 1

    def test_stress_publish(self):
        # Connect and start loop
        self.client.connect(BROKER['host'], BROKER['port'], 60)
        self.client.loop_start()
        time.sleep(2)
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

        # Measure time to publish and receive messages
        start_time = timeit.default_timer()
        for i in range(self.total_messages):
            self.client.publish(TOPIC, f"message {i}")
        time.sleep(5)  # Allow time for all messages to be received
        end_time = timeit.default_timer()

        # Assert all messages were received
        self.assertEqual(self.message_count, self.total_messages, "Not all messages were received.")
        print(f"Published and received {self.total_messages} messages in {end_time - start_time:.2f} seconds.")

        self.client.loop_stop()

    def tearDown(self):
        if self.connected:
            self.client.disconnect()

if __name__ == '__main__':
    unittest.main()