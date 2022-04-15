import paho.mqtt.client as paho
import time
import sys


def led(l):
    client = paho.Client()

    if client.connect("10.0.0.126", 1883, 60) != 0:
        print("Could ont connect to MQTT Broker!")
        sys.exit(-1)
    if l == 1:
        client.publish("top/esp32", '{“lightStatus”:“ON”}', 0)
        time.sleep(0.1)
        print(1)
    client.disconnect() 


