from abc import abstractmethod

from gmqtt import Client as MQTTClient
import easy_mqtt as easy
import asyncio
import json

class MqttAbstract:

    current_state = ""

    def createMQTTJason(self, loc, device, value, device_id):
        data = {
            "loc": loc,
            "device": device,
            "id": device_id,
            "value": value,
        }
        return json.dumps(data)

    @abstractmethod
    def on_message(self, client: MQTTClient, topic, payload, qos, properties):
        message = payload.decode()
        msg_json = json.loads(message)
        msg_id = msg_json["id"]
        msg_loc = msg_json["loc"]
        msg_device = msg_json["device"]
        msg_value = msg_json["value"]

        #irgwas mit den values machen
        status = f"wurde auf {self.current_state} gesetzt"
        self.current_state = msg_value

        #internes print out
        output = f"{self.devicename}:{msg_id} {msg_loc} {status}"
        print(output)

        #status zurückschicken
        client.publish(f"home/{self.loc}", self.createMQTTJason(self.loc, msg_device, self.current_state, self.device_id), qos=0)

    def __init__(self, loc, device_id, host, device):
        self.loc = loc
        self.device_id = device_id
        self.host = host
        self.devicename = device

    async def init_client(self):
        subscribe = f"home/{self.loc}/{self.devicename}/{self.device_id}"
        client = MQTTClient(f"{self.loc}_{self.devicename}_{self.device_id}")
        ec = easy.EasyMqtt(client)
        ec.client.on_message = self.on_message

        await ec.connect(self.host)
        ec.subscribe(subscribe, qos=0)

        while True:
            await asyncio.sleep(1)
