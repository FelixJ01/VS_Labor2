from gmqtt import Client as MQTTClient
import os
import signal
import time
import easy_mqtt as easy
import asyncio


def print_test(message):
    print(message)

async def main(broker_host):

    host = 'localhost'

    calldict = {
        'home/og/licht': print_test,
    }
    client = MQTTClient("dennis")

    easyClient = easy.EasyMqtt(client, calldict)

    client.on_connect = easyClient.on_connect
    client.on_message = easyClient.on_message
    client.on_disconnect = easyClient.on_disconnect
    client.on_subscribe = easyClient.on_subscribe
    await client.connect(broker_host)

    client.publish('home/og/licht', str('dunkel'), qos=1)
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
    host = 'localhost'
    asyncio.run((main(host)))


