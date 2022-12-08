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


def react_on_message(message):
    print(message)

async def init_client():
    host = 'localhost'

    calldict = {
        'home/og/licht': react_on_message,
    }
    client = MQTTClient("felix")

    easyClient = easy.EasyMqtt(client, calldict)

    client.on_connect = easyClient.on_connect
    client.on_message = easyClient.on_message
    client.on_disconnect = easyClient.on_disconnect
    client.on_subscribe = easyClient.on_subscribe
    client.subscribe('home/og/licht', qos=0)


    #client.publish('licht', str('dunkel'), qos=1)

    await client.connect(host)
    await asyncio.sleep(1)




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
    [sg.Text('Thermostat'), sg.Text(eg_thermostat)],
    [sg.Text('Fenster 1'), sg.Text(returnKontaktJalousi(eg_fensterkontakt1)),
     sg.Text('Fenster 2'), sg.Text(returnKontaktJalousi(eg_fensterkontakt2))],
    [sg.Text('Jalousi'), sg.Text(returnKontaktJalousi(eg_jalousi))],
    [sg.Text('Licht'), sg.Text(), sg.Text(getLicht(eg_licht))],
    [sg.Text('')],
    [sg.Text('Obergeschoss')],
    [sg.Text('Thermostat'), sg.Text(og_thermostat)],
    [sg.Text('Fenster 1'), sg.Text(returnKontaktJalousi(og_fensterkontakt1)),
     sg.Text('Fenster 2'), sg.Text(returnKontaktJalousi(og_fensterkontakt2))],
    [sg.Text('Jalousi'), sg.Text(returnKontaktJalousi(og_jalousi))],
    [sg.Text('Licht'), sg.Text(), sg.Text(getLicht(og_licht))]
]

window = sg.Window('Overview', layout, size=(400, 300))


async def main():
    await asyncio.gather(init_client())

    while True:
        event, values = window.read()
    await asyncio.sleep(1)




if __name__ == "__main__":
    asyncio.gather((main()))