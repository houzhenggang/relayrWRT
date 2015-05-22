#!/usr/bin/env python
""" Prototyping some functions neccesary for the SomaBar, like controlling
    gpios, I2C, connecting to mqtt broker, SPI controll for the RFID transceiver,
     etc.
"""

import paho.mqtt.client as mqtt
import commands
import sys
from modules.gpio import *

LED_PATH = '/sys/devices/gpio-leds.4/leds/wrtnode:blue:indicator/brightness'
out20 = ''


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from
        the server."""
    # print("Connected with result code %d" % rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/somabar/#")


def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server."""

    print('MsgRcv: %s %s' % (msg.topic, msg.payload))
    if (msg.topic == 'somabar/led'):
        if msg.payload == 'ON':
            # print "Led ON"
            commands.getoutput('echo "0" > ' + LED_PATH)
            out20.set()
        if msg.payload == 'OFF':
            # print "Led OFF"
            commands.getoutput('echo "1" > ' + LED_PATH)
            out20.clear()


def start_client():

    client = mqtt.Client(client_id="wrtnodeclient")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("127.0.0.1", 1883)
    except:
        print "Error: Couldn't connect to the broker, check credentials!"

        global out20
    try:
        out20 = DigitalIO.get_output(GPIO20)    # export GPIO20 as output
    except:
        print "File not found, check that your platform supports GPIO20" \
                "and that the gpio kernet module is loaded"

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    start_client()
