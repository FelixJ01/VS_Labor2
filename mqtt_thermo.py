from mqtt_abstract import MqttAbstract
import json

class MqttThermo(MqttAbstract):

    current_state = "20"

    def on_message(self, client, topic, payload, qos, properties):
        message = payload.decode()
        msg_json = json.loads(message)
        msg_id = msg_json["id"]
        msg_loc = msg_json["loc"]
        msg_device = msg_json["device"]
        msg_value = msg_json["value"]

        # irgwas mit den values machen
        status = ""
        if msg_value.isdecimal():
            int_val = int(msg_value)
            if 24 > int_val > 15:
                self.current_state = msg_value
                status = f"wurde auf {self.current_state} gesetzt"
            else:
                status = "eingabe außerhalb 7-24, temperatur nicht geändert"
        else:
            status = "ungültige eingabe, temperatur nicht geändert"


        output = f"{self.devicename}:{msg_id} {msg_loc} {status}"
        print(output)

        # status zurückschicken
        client.publish(f"home/{self.loc}",
                       self.createMQTTJason(self.loc, msg_device, self.current_state, self.device_id), qos=0)
    pass
