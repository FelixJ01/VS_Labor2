import PySimpleGUI as sg
from gmqtt import Client as MQTTClient
import easy_mqtt as easy
import asyncio
import json


window_dict = {
    "eg_1" : False,
    "eg_2" : False,
    "og_1" : False,
    "og_2" : False,
}

thermo_dict = {
    "eg_1": "20",
    "og_1": "20",
}

eg_thermostat = 0
eg_jalousie = False
eg_licht = False

og_thermostat = 0
og_jalousie = False
og_licht = False


ec: easy.EasyMqtt


def on_message(client: MQTTClient, topic, payload, qos, properties):
    global window_dict, thermo_dict

    message = payload.decode()
    msg_json = json.loads(message)
    msg_id = msg_json["id"]
    msg_loc = msg_json["loc"]
    msg_value = msg_json["value"]
    msg_device = msg_json["device"]

    if "window" in msg_device:
        window_dict[f"{msg_loc}_{msg_id}"] = msg_value
    if "thermo" in msg_device:
        thermo_dict[f"{msg_loc}_{msg_id}"] = msg_value

    print(f"got message: {message}")


async def init_client():
    global ec
    host = 'localhost'
    client = MQTTClient("Dashboard")
    ec = easy.EasyMqtt(client)
    ec.client.on_message = on_message

    await client.connect(host)
    ec.subscribe("home/#", qos=0)


def returnKontaktJalousi(bool):
    if(bool):
        return "Auf"
    else:
        return "Zu"


def getLicht(bool):
    if (bool):
        return "An"
    else:
        return "Aus"

    
def createMQTTJason(loc, device, device_id, value):
    data = {
        "loc": loc,
        "device": device,
        "id":  device_id,
        "value": value,
    }
    return json.dumps(data)


layout = [
    [sg.Text('Erdgeschoss')],
    [sg.Text('Thermostat', key='eg_thermostat_1_text'), sg.InputText("20", key="eg_thermostat_1", size=(10, 2)), sg.Button("OK", key="eg_thermo_1_button")],
    [sg.Text('Fenster 1', key='eg_fenster_1_text'), sg.Text(returnKontaktJalousi(window_dict["eg_1"]), key='eg_window_1_state') , sg.Button("get status", key="eg_fenster_1_button")],
    [sg.Text('Fenster 2', key='eg_fenster_2_text'),sg.Text(returnKontaktJalousi(window_dict["eg_2"]), key='eg_window_2_state') , sg.Button("get status", key="eg_fenster_2_button")],
    [sg.Text('Jalousie', key='eg_jalousi_1_text'), sg.Button(returnKontaktJalousi(eg_jalousie), key="eg_jalousie_1_button")],
    [sg.Text('Licht', key='eg_licht_1_text'), sg.Button(getLicht(eg_licht), key="eg_licht_1_button")],
    [],
    [sg.Text('Obergeschoss')],
    [sg.Text('Thermostat', key='og_thermostat_1_text'), sg.InputText("20", key="og_thermostat_1", size=(10, 2)), sg.Button("OK", key="og_thermo_1_button")],
    [sg.Text('Fenster 1', key='og_fenster_1_text'), sg.Text(returnKontaktJalousi(window_dict["og_1"]), key='og_window_1_state') , sg.Button("get status",  key="og_fenster_1_button")],
    [sg.Text('Fenster 2', key='og_fenster_2_text'), sg.Text(returnKontaktJalousi(window_dict["eg_2"]), key='og_window_2_state') , sg.Button("get status",  key="og_fenster_2_button")],
    [sg.Text('Jalousie', key='og_jalousi_1_text'), sg.Button(returnKontaktJalousi(og_jalousie), key="og_jalousie_1_button")],
    [sg.Text('Licht', key='og_licht_1_text'), sg.Button(getLicht(og_licht), key="og_licht_1_button")],
    [],
    [],
    [sg.Button("verlasse das haus", key="routine_leave_home")],
    [sg.Button("guten morgen", key="routine_good morning")]
]


def updateButtonText(window, windowKey , text):
    window[windowKey].Update(text=text)


def send_message(floor, device, id, value):
    global ec
    ec.publish(f"home/{floor}/{device}/{id}", createMQTTJason(f"{floor}", f"{device}", id, value), qos=1)


async def warn_open_window(window):
    global window_dict
    send_message("eg", "window", 1, True)
    send_message("eg", "window", 2, True)
    send_message("og", "window", 1, True)
    send_message("og", "window", 2, True)

    await asyncio.sleep(0.5)
    anyopen = False
    open_list = []
    for cur_win in window_dict.keys():
        is_open = window_dict[cur_win]
        if is_open:
            anyopen = True
            open_list.append(f"window {cur_win}")
    if anyopen:
        window.Popup(f"{open_list} still open!! ")


async def leave_house_routine(window):
    send_message("eg", "thermo", 1, "15")
    send_message("og", "thermo", 1, "15")

    send_message("eg", "light", 1, False)
    send_message("og", "light", 1, False)

    send_message("eg", "jalousie", 1, False)
    send_message("og", "jalousie", 1, False)

    await warn_open_window(window)

async def good_morning_routine(window, sg):
    global thermo_dict
    send_message("og", "light", 1, True)
    send_message("og", "jalousie", 1, True)
    send_message("og", "thermo", 1, "22")

    await asyncio.sleep(0.5)

    updated_temperature = thermo_dict["og_1"]
    sg["og_thermostat_1"].Update(updated_temperature)
    window.Popup(f"Good morning!! temperature was set to {updated_temperature}")

async def main_window():
    global eg_licht, eg_jalousie, eg_thermostat
    global og_licht, og_jalousie, og_thermostat
    global ec, window_dict

    sg.theme("Dark")
    window = sg.Window('Overview', layout, size=(400, 500))

    while True:
        window.refresh()
        event, values = window.read(timeout = 0)
        if event == sg.WINDOW_CLOSED:
            break

        ## Routine
        if event == "routine_leave_home":
            await leave_house_routine(sg)

        if event == "routine_good morning":
            await good_morning_routine(sg, window)

        ## EG
        if event == "eg_thermo_1_button":
            send_message("eg", "thermo", 1,  values["eg_thermostat_1"])

        if event == "eg_fenster_1_button":
            send_message("eg", "window", 1, True)
            await asyncio.sleep(0.5)
            window["eg_window_1_state"].Update(returnKontaktJalousi(window_dict["eg_1"]))

        if event == "eg_fenster_2_button":
            send_message("eg", "window", 2, True)
            await asyncio.sleep(0.5)
            window["eg_window_2_state"].Update(returnKontaktJalousi(window_dict["eg_2"]))

        if event == "eg_jalousie_1_button":
            eg_jalousie = not eg_jalousie
            updateButtonText(window, event, returnKontaktJalousi(eg_jalousie))
            send_message("eg", "jalousie", 1, eg_jalousie)

        if event == "eg_licht_1_button":
            eg_licht = not eg_licht
            updateButtonText(window, event, getLicht(eg_licht))
            send_message("eg", "light", 1, eg_licht)
        ## OG
        if event == "og_thermo_1_button":
            send_message("og", "thermo", 1,  values["og_thermostat_1"])

        if event == "og_fenster_1_button":
            send_message("og", "window", 1, True)
            await asyncio.sleep(0.5)
            window["og_window_1_state"].Update(returnKontaktJalousi(window_dict["og_1"]))

        if event == "og_fenster_2_button":
            send_message("og", "window", 2, True)
            await asyncio.sleep(0.5)
            window["og_window_2_state"].Update(returnKontaktJalousi(window_dict["og_2"]))

        if event == "og_jalousie_1_button":
            og_jalousie = not og_jalousie
            updateButtonText(window, event, returnKontaktJalousi(og_jalousie))
            send_message("og", "jalousie", 2, og_jalousie)

        if event == "og_licht_1_button":
            og_licht = not og_licht
            updateButtonText(window, event, getLicht(og_licht))
            send_message("og", "light", 1, og_licht)
        await asyncio.sleep(0.1)

    window.close()


async def main():
    await asyncio.gather(init_client(), main_window())

if __name__ == "__main__":
    asyncio.run((main()))
