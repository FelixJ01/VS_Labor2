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
        print('on_connect')

        # Hier muss jedes Topic, auf welches abonniert werden soll, subscribed werden.
        # Tipp: Überlegen Sie sich, wie Wildcards behandelt werden sollen
        logging.info('[CONNECTED {}]'.format(client._client_id))
       # client.subscribe('TEST/#', qos=0)

    def on_message(self, client, topic, payload, qos, properties):
     #   print('on_message')
        if topic in self.callback_dict.keys():
            fun = self.callback_dict[topic]
            fun(str(payload))
     #   print(f'topic: {topic} payload: {payload}')

        # Hier muss die Callback methode für das jeweilige Topic aufgerufen werden
        logging.info('[RECV MSG {}] TOPIC: {} PAYLOAD: {} QOS: {} PROPERTIES: {}'
                     .format(client._client_id, topic, payload, qos, properties))

    def on_disconnect(self, client, packet, exc=None):
        logging.info('[DISCONNECTED {}]'.format(client._client_id))
        print('on_disconnect')


    def on_subscribe(self, client, mid, qos, properties):
        logging.info('[SUBSCRIBED {}] QOS: {}'.format(client._client_id, qos))
        print('on_subscribe')

    def send_message(self, topic, message: bytes):
        print('send_message')
        self.client.publish(topic, str(time.time()), qos=1)

    async def connect(self, host):
        await self.client.connect(host)

    def publish(self, message_or_topic, payload=None, qos=0):
        self.client.publish(message_or_topic, payload, qos)

    def subscribe(self, topic, qos):
        self.client.subscribe(topic, qos)
