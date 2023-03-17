from os import statvfs
from time import sleep
import network
from mqtt import MQTTClient 
import machine 
import time
import json
import random
import bluetooth
import dht
from machine import Pin

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('NF702', '3006757878')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

def sub_cb(topic, msg): 
    jsonobject=json.loads(msg)
    print(jsonobject["bulb"])
    if jsonobject["bulb"]=="ON":
       led.value(1)
    elif jsonobject["bulb"]=="OFF":
        led.value(0)

led=machine.Pin(2,machine.Pin.OUT)

with open("certs/cert", 'rb') as f:
    certf = f.read()
with open("certs/privkey", 'rb') as f:
    keyf = f.read()

client = MQTTClient(client_id="esp_32_class3_nrfj_thing", server="a1ztq6e5d2o4a0-ats.iot.us-east-1.amazonaws.com", port=8883, ssl=True, ssl_params={"cert":certf, "key":keyf})
 

client.set_callback(sub_cb) 
client.connect()
client.subscribe(topic="esp32nrfj/sub")


d = dht.DHT11(Pin(15))
i=0


i = (i + 1) % 10
d.measure()
    
temp = d.temperature()
hum = d.humidity()
    
print('Temperature: {}°C\tHumidity: {}%'.format(temp, hum))
print("Sending temp/humidity data") 
client.publish(topic="esp32nrfj/dht11data", msg=json.dumps({"temp": int(temp),"hum":int(hum)}))   
    #machine.lightsleep(10000)
time.sleep(10)
client.check_msg();
     
# Configurar pines para que estén en el estado correcto
led.value(0)
# Agregar una pausa antes de entrar en modo de suspensión profunda
#time.sleep(5)
# Entrar en modo de suspensión profunda
machine.deepsleep(10000)
