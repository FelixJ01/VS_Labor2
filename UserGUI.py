
from typing import List
from enum import Enum
import PySimpleGUI as sg
from PySimpleGUI import Text, Input

eg_thermostat = 0
eg_fensterkontakt1 = False
eg_fensterkontakt2 = False
eg_jalousi = False
eg_licht = False


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
    [sg.Text('Thermostat'), sg.Text(eg_thermostat, key='eg_t'), sg.Button('<'), sg.Button('>')],
    [sg.Text('Fenster 1'), sg.Text(returnKontaktJalousi(eg_fensterkontakt1)),
     sg.Text('Fenster 2'), sg.Text(returnKontaktJalousi(eg_fensterkontakt2))],
    [sg.Text('Jalousi'), sg.Text(returnKontaktJalousi(eg_jalousi), key='eg_j'), sg.Button('Toggle Jalousi')],
    [sg.Text('Licht'), sg.Text(), sg.Text(getLicht(eg_licht), key='eg_l'), sg.Button('Toggle Licht')],
    [sg.Text('')]]

window = sg.Window('Overview', layout, size=(400, 300))
event, values = window.read()

while True:
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == '<':
        if(eg_thermostat > 0):
            eg_thermostat = eg_thermostat -1
            window['eg_t'].update(eg_thermostat)
        print("lower")
    elif event == '>':
        if(eg_thermostat < 40):
            eg_thermostat = eg_thermostat+1
            window['eg_t'].update(eg_thermostat)
        print("higher")
    elif event == 'Toggle Jalousi':
        eg_jalousi = not eg_jalousi
        window['eg_j'].update(returnKontaktJalousi(eg_jalousi))
    elif event == 'Toggle Licht':
        eg_licht = not eg_licht
        window['eg_l'].update(getLicht(eg_licht))

