import paho.mqtt.client as mqtt
import unittest
import time

BROKER = {'host': '172.16.0.72', 'port': 1883}
TOPIC = "sensor/data"

class TestMultipleMQTTClients(unittest.TestCase):

    def setUp(self):
        self.clients = []
        self.messages_received = []

    def create_client(self, client_id, message_to_send=None):
        client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
        client.on_connect = lambda c, u, f, rc: c.subscribe(TOPIC) if rc == 0 else print(f"Client {client_id} failed to connect.")
        client.on_message = lambda c, u, msg: self.messages_received.append((client_id, msg.payload.decode()))
        client.connect(BROKER['host'], BROKER['port'], 60)
        if message_to_send:
            client.publish(TOPIC, message_to_send)
        self.clients.append(client)

    def test_multiple_clients(self):
        # Create multiple clients and publish messages
        self.create_client("client_1", "message_from_client_1")
        self.create_client("client_2", "message_from_client_2")
        self.create_client("client_3", "message_from_client_3")

        # Start all clients
        for client in self.clients:
            client.loop_start()

        # Wait for messages
        time.sleep(3)

        # Check received messages
        expected_messages = [
            ("client_1", "message_from_client_1"),
            ("client_2", "message_from_client_2"),
            ("client_3", "message_from_client_3")
        ]
        for expected in expected_messages:
            self.assertIn(expected, self.messages_received)

        # Stop all clients
        for client in self.clients:
            client.loop_stop()

    def tearDown(self):
        for client in self.clients:
            client.disconnect()


if __name__ == '__main__':
    unittest.main()
