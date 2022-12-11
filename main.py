import mqtt_light as light_endpoint
import mqtt_thermo as thermo_endpoint
import mqtt_window as window_endpoint
import mqtt_jalousie as jalousie_endpoint
import SensorGUI
import asyncio


async def main():
    instance_list = [
        # windows
        window_endpoint.MqttWindow("og", 1, "localhost", "window").init_client(),
        window_endpoint.MqttWindow("og", 2, "localhost", "window").init_client(),
        window_endpoint.MqttWindow("eg", 1, "localhost", "window").init_client(),
        window_endpoint.MqttWindow("eg", 2, "localhost", "window").init_client(),
        # lights
        light_endpoint.MqttLight("eg", 1, "localhost", "light").init_client(),
        light_endpoint.MqttLight("og", 1, "localhost", "light").init_client(),
        # jalousie
        jalousie_endpoint.MqttJalousie("eg", 1, "localhost", "jalousie").init_client(),
        jalousie_endpoint.MqttJalousie("og", 1, "localhost", "jalousie").init_client(),
        # thermostat
        thermo_endpoint.MqttThermo("eg", 1, "localhost", "thermo").init_client(),
        thermo_endpoint.MqttThermo("og", 1, "localhost", "thermo").init_client(),
        # gui
        SensorGUI.init_client(),
        SensorGUI.main_window()
    ]

    await asyncio.gather(
        *instance_list
    )

    while True:

        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run((main()))


