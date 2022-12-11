import PySimpleGUI as sg
import PySimpleGUI.PySimpleGUI
from gmqtt import Client as MQTTClient
import easy_mqtt as easy
import asyncio
import json


ec: easy.EasyMqtt
win: PySimpleGUI.PySimpleGUI.Window

device_dict = {
    "eg_1_window" : False,
    "eg_2_window" : False,
    "og_1_window" : False,
    "og_2_window" : False,
    "eg_1_thermo": "20",
    "og_1_thermo": "20",
    "eg_1_jalousie": False,
    "og_1_jalousie": False,
    "eg_1_light": False,
    "og_1_light": False,
}


def on_message(client: MQTTClient, topic, payload, qos, properties):
    global device_dict, win

    message = payload.decode()
    msg_json = json.loads(message)
    msg_id = msg_json["id"]
    msg_loc = msg_json["loc"]
    msg_value = msg_json["value"]
    msg_device = msg_json["device"]

    key = f"{msg_loc}_{msg_id}_{msg_device}"
    device_dict[key] = msg_value

    if "jalousie" in key:
        win[key].Update(text=returnKontaktJalousi(msg_value))
    elif "light" in key:
        win[key].Update(text=get_licht(msg_value))
    elif "window" in key:
        win[key].Update(returnKontaktJalousi(msg_value))
    else:
        win[key].Update(msg_value)

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


def get_licht(val):
    if val:
        return "An"
    else:
        return "Aus"


def create_json(loc, device, device_id, value):
    data = {
        "loc": loc,
        "device": device,
        "id":  device_id,
        "value": value,
    }
    return json.dumps(data)


layout = [
    [sg.Text('Erdgeschoss')],
    [sg.Text('Thermostat'), sg.InputText("20", key="eg_1_thermo", size=(10, 2)), sg.Button("OK", key="eg_thermo_1_button")],
    [sg.Text('Fenster 1'), sg.Text(returnKontaktJalousi(device_dict["eg_1_window"]), key='eg_1_window') , sg.Button("get status", key="eg_fenster_1_button")],
    [sg.Text('Fenster 2'),sg.Text(returnKontaktJalousi(device_dict["eg_2_window"]), key='eg_2_window') , sg.Button("get status", key="eg_fenster_2_button")],
    [sg.Text('Jalousie'), sg.Button(returnKontaktJalousi(device_dict["eg_1_jalousie"],), key="eg_1_jalousie")],
    [sg.Text('Licht'), sg.Button(get_licht(device_dict["eg_1_light"], ), key="eg_1_light")],
    [],
    [sg.Text('Obergeschoss')],
    [sg.Text('Thermostat'), sg.InputText("20", key="og_1_thermo", size=(10, 2)), sg.Button("OK", key="og_thermo_1_button")],
    [sg.Text('Fenster 1'), sg.Text(returnKontaktJalousi(device_dict["og_1_window"]), key='og_1_window') , sg.Button("get status",  key="og_fenster_1_button")],
    [sg.Text('Fenster 2'), sg.Text(returnKontaktJalousi(device_dict["og_2_window"]), key='og_2_window') , sg.Button("get status",  key="og_fenster_2_button")],
    [sg.Text('Jalousie'), sg.Button(returnKontaktJalousi(device_dict["og_1_jalousie"],), key="og_1_jalousie")],
    [sg.Text('Licht'), sg.Button(get_licht(device_dict["og_1_light"]), key="og_1_light")],
    [],
    [],
    [sg.Button("verlasse das haus", key="routine_leave_home")],
    [sg.Button("guten morgen", key="routine_good morning")]
]


def send_message(floor, device, device_id, value):
    global ec
    ec.publish(f"home/{floor}/{device}/{device_id}", create_json(f"{floor}", f"{device}", device_id, value), qos=1)


async def warn_open_window(window):
    global device_dict, win
    send_message("eg", "window", 1, True)
    send_message("eg", "window", 2, True)
    send_message("og", "window", 1, True)
    send_message("og", "window", 2, True)

    await asyncio.sleep(0.5)
    any_open = False
    open_list = []
    for cur_win in device_dict.keys():
        if "window" in cur_win:
            is_open = device_dict[cur_win]
            if is_open:
                any_open = True
                open_list.append(f"{cur_win}")
    if any_open:
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
    global device_dict
    send_message("og", "light", 1, True)
    send_message("og", "jalousie", 1, True)
    send_message("og", "thermo", 1, "22")

    await asyncio.sleep(0.5)

    updated_temperature = device_dict["og_1_thermo"]
    sg["og_1_thermo"].Update(updated_temperature)
    window.Popup(f"Good morning!! temperature was set to {updated_temperature}")


async def main_window():
    global ec, win

    sg.theme("Dark")
    window = sg.Window('Overview', layout, size=(400, 500))
    win = window
    while True:
        window.refresh()
        event, values = window.read(timeout = 0)
        if event == sg.WINDOW_CLOSED:
            break

        # Routine ---------------------------------
        if event == "routine_leave_home":
            await leave_house_routine(sg)

        if event == "routine_good morning":
            await good_morning_routine(sg, window)

        # EG ---------------------------------
        if event == "eg_thermo_1_button":
            send_message("eg", "thermo", 1,  values["eg_1_thermo"])

        if event == "eg_fenster_1_button":
            send_message("eg", "window", 1, True)

        if event == "eg_fenster_2_button":
            send_message("eg", "window", 2,True)

        if event == "eg_1_jalousie":
            send_message("eg", "jalousie", 1, not device_dict[event])

        if event == "eg_1_light":
            send_message("eg", "light", 1, not device_dict[event])
        # OG ---------------------------------
        if event == "og_thermo_1_button":
            send_message("og", "thermo", 1, values["og_1_thermo"])

        if event == "og_fenster_1_button":
            send_message("og", "window", 1, True)

        if event == "og_fenster_2_button":
            send_message("og", "window", 2, True)

        if event == "og_1_jalousie":
            send_message("og", "jalousie", 1, not device_dict[event])

        if event == "og_1_light":
            send_message("og", "light", 1, not device_dict[event])
        await asyncio.sleep(0.1)

    window.close()
