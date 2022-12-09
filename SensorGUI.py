from typing import List
from enum import Enum
import PySimpleGUI as sg
from PySimpleGUI import Text, Input
from gmqtt import Client as MQTTClient
import os
import signal
import time
import easy_mqtt as easy
import asyncio


eg_thermostat = 0
eg_fensterkontakt1 = False
eg_fensterkontakt2 = False
eg_jalousi = False
eg_licht = False

og_thermostat = 0
og_fensterkontakt1 = False
og_fensterkontakt2 = False
og_jalousi = False
og_licht = False

def react_on_light(message):
    print(message)

def react_on_jalousi(message):
    print(message)

def react_on_window(message):
    print(message)


ec: easy.EasyMqtt


async def init_client():
    global ec
    host = 'localhost'
    calldict = {
        'light': react_on_light,
        'window': react_on_jalousi,
        'jalousi': react_on_window,
    }
    client = MQTTClient("felix")
    ec = easy.EasyMqtt(client, calldict)
    await client.connect(host)


def returnKontaktJalousi(bool):
    if(bool):
        return "Zu"
    else:
        return "Auf"

def getLicht(bool):
    if (bool):
        return "An"
    else:
        return "Aus"



layout = [
    [sg.Text('Erdgeschoss')],
    [sg.Text('Thermostat', key='eg_thermostat_1_text'), sg.Text(eg_thermostat, key="eg_thermostat_1")],
    [sg.Text('Fenster 1', key='eg_fenster_1_text'), sg.Button(returnKontaktJalousi(eg_fensterkontakt1), key="eg_fenster_1_button")],
    [sg.Text('Fenster 2', key='eg_fenster_2_text'), sg.Button(returnKontaktJalousi(eg_fensterkontakt2), key="eg_fenster_2_button")],
    [sg.Text('Jalousi', key='eg_jalousi_1_text'), sg.Button(returnKontaktJalousi(eg_jalousi), key="eg_jalousi_1_button")],
    [sg.Text('Licht', key='eg_licht_1_text'), sg.Button(getLicht(eg_licht), key="eg_licht_1_button")],
    [],
    [sg.Text('Obergeschoss')],
    [sg.Text('Thermostat', key='og_thermostat_1_text'), sg.Text(og_thermostat, key="og_thermostat_1")],
    [sg.Text('Fenster 1', key='og_fenster_1_text'), sg.Button(returnKontaktJalousi(og_fensterkontakt1), key="og_fenster_1_button")],
    [sg.Text('Fenster 2', key='og_fenster_2_text'), sg.Button(returnKontaktJalousi(og_fensterkontakt2), key="og_fenster_2_button")],
    [sg.Text('Jalousi', key='og_jalousi_1_text'), sg.Button(returnKontaktJalousi(og_jalousi), key="og_jalousi_1_button")],
    [sg.Text('Licht', key='og_licht_1_text'), sg.Button(getLicht(og_licht), key="og_licht_1_button")],
]

def updateButtonText(window, windowKey , text):
    window[windowKey].Update(text=text)

def publishMessage(topic, payload):
    global ec
    ec.publish(topic, payload, qos=1)


async def main_window():
    global eg_fensterkontakt1, eg_fensterkontakt2, eg_licht, eg_jalousi, eg_thermostat
    global og_fensterkontakt1, og_fensterkontakt2, og_licht, og_jalousi, og_thermostat
    global ec

    sg.theme("Dark")
    window = sg.Window('Overview', layout, size=(400, 500))

    while True:
        window.refresh()
        event, values = window.read(timeout = 0)
        if event == sg.WINDOW_CLOSED:
            break
        ## EG
        if event == "eg_fenster_1_button":
            eg_fensterkontakt1 = not eg_fensterkontakt1
            updateButtonText(window, event, returnKontaktJalousi(eg_fensterkontakt1))
            publishMessage("window",  str(f'{eg_fensterkontakt1}'))
        if event == "eg_fenster_2_button":
            eg_fensterkontakt2 = not eg_fensterkontakt2
            updateButtonText(window, event, returnKontaktJalousi(eg_fensterkontakt2))
            publishMessage("window", str(f'{eg_fensterkontakt1}'))
        if event == "eg_jalousi_1_button":
            eg_jalousi = not eg_jalousi
            updateButtonText(window, event, returnKontaktJalousi(eg_jalousi))
            publishMessage("jalousi", str(f'{eg_jalousi}'))
        if event == "eg_licht_1_button":
            eg_licht = not eg_licht
            updateButtonText(window, event, getLicht(eg_licht))
            publishMessage("light", str(f'{eg_licht}'))
        ## OG
        if event == "og_fenster_1_button":
            og_fensterkontakt1 = not og_fensterkontakt1
            updateButtonText(window, event, returnKontaktJalousi(og_fensterkontakt1))
            publishMessage("window",  str(f'{og_fensterkontakt1}'))
        if event == "og_fenster_2_button":
            og_fensterkontakt2 = not og_fensterkontakt2
            updateButtonText(window, event, returnKontaktJalousi(og_fensterkontakt2))
            publishMessage("window", str(f'{og_fensterkontakt1}'))
        if event == "og_jalousi_1_button":
            og_jalousi = not og_jalousi
            updateButtonText(window, event, returnKontaktJalousi(og_jalousi))
            publishMessage("jalousi", str(f'{og_jalousi}'))
        if event == "og_licht_1_button":
            og_licht = not og_licht
            updateButtonText(window, event, getLicht(og_licht))
            publishMessage("light", str(f'{og_licht}'))
        await asyncio.sleep(0.1)

    window.close()


async def main():
    await asyncio.gather(init_client(), main_window())

if __name__ == "__main__":
    asyncio.run((main()))
