from gmqtt import Client as MQTTClient
import os
import signal
import time
import easy_mqtt as easy
import asyncio


def print_test(message):
    print(message)

def callback_dict_light(message):
    print(f'getmessage: light {message}')

def callback_dict_window(message):
    print(f'getmessage: window {message}')

def callback_dict_jalousi(message):
    print(f'getmessage: jalousi {message}')

async def main():

    host = 'localhost'
    calldict = {
        'light': callback_dict_light,
        'window': callback_dict_window,
        'jalousi': callback_dict_jalousi,
    }

    client = MQTTClient("dennis")
    ec = easy.EasyMqtt(client, calldict)
    await ec.connect(host)

    ec.subscribe('light', qos=0)
    ec.subscribe('window', qos=0)
    ec.subscribe('jalousi', qos=0)

    while True:
       # ec.publish('light', str("dunkel"), qos=1)
       # await asyncio.sleep(2)
       # ec.publish('light', str("hell"), qos=1)
        await asyncio.sleep(1)


 #   client2 = MQTTClient("dennis")

#    easyClient2 = easy.EasyMqtt(client2, calldict)

    #client2.on_connect = easyClient2.on_connect
   # client2.on_message = easyClient2.on_message
  #  client2.on_disconnect = easyClient2.on_disconnect
 #   client2.on_subscribe = easyClient2.on_subscribe
##    await client2.connect(broker_host)



    # self.client.subscribe('TEST/#', qos=0)

 #   client2.subscribe('licht', qos=0)
 #   client.subscribe('TEST/TIME', qos=0)


  #  client.publish('licht', str('dunkel'), qos=1)
  #  client2.publish('TEST/TIME', str(time.time()), qos=1)




if __name__ == "__main__":
    asyncio.run((main()))


