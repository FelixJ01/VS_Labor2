import gmqtt
import logging

class EasyMqtt:

    def on_message_callback(self, message):
        print(f"got message: {message}")

    def __init__(self, client: gmqtt.Client):
        self.client = client
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe

    def on_message(self, client, topic, payload, qos, properties):
        self.on_message_callback(payload.decode())

    def on_connect(self, client, flags, rc, properties):
        print(f'on_connect {client._client_id}')

    def on_disconnect(self, client, packet, exc=None):
        print(f'on_disconnect {client._client_id}')

    def on_subscribe(self, client, mid, qos, properties):
        logging.info('[SUBSCRIBED {}] QOS: {}'.format(client._client_id, qos))

    async def connect(self, host):
        await self.client.connect(host)

    def publish(self, message_or_topic, payload=None, qos=0):
        self.client.publish(message_or_topic, payload, qos)

    def subscribe(self, topic, qos):
       ## print(f'subscribed to: {topic}')
        self.client.subscribe(topic, qos, no_local=True)
