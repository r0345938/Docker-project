import paho.mqtt.client as mqtt
import unittest
import time

BROKER = {'host': '172.16.0.72', 'port': 1883}
MULTIPLE_TOPICS = ["sensor/data", "sensor/status"]

class TestMQTTMultipleTopics(unittest.TestCase):

    def setUp(self):
        self.client = mqtt.Client(client_id="test_multiple_topics", protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.connected = False
        self.received_messages = {topic: None for topic in MULTIPLE_TOPICS}

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected successfully to broker.")
            for topic in MULTIPLE_TOPICS:
                client.subscribe(topic)
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
        self.received_messages[msg.topic] = msg.payload.decode()

    def test_multiple_topics(self):
        # Connect and start loop
        self.client.connect(BROKER['host'], BROKER['port'], 60)
        self.client.loop_start()
        time.sleep(2)
        self.assertTrue(self.connected, "MQTT Broker connection failed.")

        # Publish messages to multiple topics
        messages = {"sensor/data": "data_message", "sensor/status": "status_message"}
        for topic, message in messages.items():
            self.client.publish(topic, message)
        time.sleep(2)

        # Verify messages were received
        for topic, expected_message in messages.items():
            self.assertEqual(self.received_messages[topic], expected_message,
                             f"Message for topic {topic} did not match.")

        self.client.loop_stop()

    def tearDown(self):
        if self.connected:
            self.client.disconnect()


if __name__ == '__main__':
    unittest.main()
