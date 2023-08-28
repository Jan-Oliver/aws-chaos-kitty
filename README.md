### Install

Todo - Add setup instructions for a python virtual environment

Install RPIO
sudo apt-get -y install python3-rpi.gpio

### Neopixels
https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka
sudo python3 -m pip install --force-reinstall adafruit-blinka

### MQTT

pip install awsiot
pip install awscrt
https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/mqtt5_pubsub.md

Button:
sudo apt-get install python3-dev python3-rpi.gpio
pip install RPi.GPIO

General:
sudo python3 -m pip install --force-reinstall adafruit-blinka


Reference

LED stripe: schnidrc@chaoskitty:~/rpi-ws281x-python/examples $ sudo python3 strandtest.py




#!/bin/bash

python3 mqtt5_pubsub.py --endpoint a2f97hrgv6egz9-ats.iot.eu-central-1.amazonaws.com --cert 4cd4ee53ab6b0dff22c32f9acaa08221ad1dd4d58dbb34ba889b6a7
f77b2b6d0-certificate.pem.crt --key 4cd4ee53ab6b0dff22c32f9acaa08221ad1dd4d58dbb34ba889b6a7f77b2b6d0-private.pem.key --client_id Raspi4 

~/mqtt $ more mqtt.sh 
execute it ./mqtt.sh
