import json
from mqtt_abstract import MqttAbstract


class MqttWindow(MqttAbstract):

    current_state = True

    def on_message(self, client, topic, payload, qos, properties):
        state = "offen" if not self.current_state else "geschlossen"
        message = payload.decode()
        msg_json = json.loads(message)
        msg_id = msg_json["id"]
        msg_loc = msg_json["loc"]

        # irgwas mit den values machen
        status = f"is {state}"
        output = f"{self.devicename}:{msg_id} {msg_loc} {status}"
        print(output)

        # status zurückschicken
        client.publish(f"home/{self.loc}", self.createMQTTJason(self.loc, self.devicename, self.current_state, self.device_id), qos=0)
    pass
