import mqtt_light as light_endpoint
import mqtt_thermo as thermo_endpoint
import mqtt_window as window_endpoint
import mqtt_jalousie as jalousie_endpoint
import SensorGUI
import asyncio


async def main():

    og_fenster_1 = window_endpoint.MqttWindow("og", 1, "localhost", "window")
    og_fenster_2 = window_endpoint.MqttWindow("og", 2, "localhost", "window")
    eg_fenster_1 = window_endpoint.MqttWindow("eg", 1, "localhost", "window")
    eg_fenster_2 = window_endpoint.MqttWindow("eg", 2, "localhost", "window")

    eg_light_1 = light_endpoint.MqttLight("eg", 1, "localhost", "light")
    og_light_1 = light_endpoint.MqttLight("og", 1, "localhost", "light")

    eg_jalousie_1 = jalousie_endpoint.MqttJalousie("eg", 1, "localhost", "jalousie")
    og_jalousie_1 = jalousie_endpoint.MqttJalousie("og", 1, "localhost", "jalousie")

    eg_thermo_1 = thermo_endpoint.MqttThermo("eg", 1, "localhost", "thermo")
    og_thermo_1 = thermo_endpoint.MqttThermo("og", 1, "localhost", "thermo")

    asyncio.gather(
    og_fenster_1.init_client(),
    og_fenster_2.init_client(),
    eg_fenster_1.init_client(),
    eg_fenster_2.init_client(),
    eg_light_1.init_client(),
    og_light_1.init_client(),
    eg_jalousie_1.init_client(),
    og_jalousie_1.init_client(),
    eg_thermo_1.init_client(),
    og_thermo_1.init_client(),
    SensorGUI.init_client(),
    SensorGUI.main_window()
    )

    while True:

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run((main()))


