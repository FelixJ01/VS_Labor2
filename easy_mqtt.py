import gmqtt
from gmqtt import Client as MQTTClient

import logging
import os
import signal
import time
import asyncio
from gmqtt import Client as MQTTClient

# Es muss der MqttClient initialisiert werden
# Der Start der Verbindung muss asynchron erfolgen. Siehe Beispiel in der gmqtt Doku
class EasyMqtt:

    def __init__(self, client: gmqtt.Client, callback_dict):  # Überlegen Sie, welche Klassenvariablen noch gebraucht werden
        self.callback_dict = callback_dict
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.on_subscribe = self.on_subscribe
        self.client = client

    def on_connect(self, client, flags, rc, properties):
        print(f'on_connect {client._client_id}')

        # Hier muss jedes Topic, auf welches abonniert werden soll, subscribed werden.
        # Tipp: Überlegen Sie sich, wie Wildcards behandelt werden sollen
        logging.info('[CONNECTED {}]'.format(client._client_id))
       # client.subscribe('TEST/#', qos=0)

    def on_message(self, client, topic, payload, qos, properties):
        if topic in self.callback_dict.keys():
            fun = self.callback_dict[topic]
            fun(str(payload))
        # Hier muss die Callback methode für das jeweilige Topic aufgerufen werden
        logging.info('[RECV MSG {}] TOPIC: {} PAYLOAD: {} QOS: {} PROPERTIES: {}'
                     .format(client._client_id, topic, payload, qos, properties))

    def on_disconnect(self, client, packet, exc=None):
        logging.info('[DISCONNECTED {}]'.format(client._client_id))
        print(f'on_disconnect {client._client_id}')


    def on_subscribe(self, client, mid, qos, properties):
        logging.info('[SUBSCRIBED {}] QOS: {}'.format(client._client_id, qos))
        print('on_subscribe')

    def send_message(self, topic, message: bytes):
        print(f'send_message: {str(message)}')
        self.client.publish(topic, str(time.time()), qos=1)

    async def connect(self, host):
        await self.client.connect(host)

    def publish(self, message_or_topic, payload=None, qos=0):
        print(f'send_message: {message_or_topic} {str(payload)}')

        self.client.publish(message_or_topic, payload, qos)

    def subscribe(self, topic, qos):
        print(f'subscribed to: {topic}')
        self.client.subscribe(topic, qos)
