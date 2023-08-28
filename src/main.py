#!/usr/bin/env python3
import signal
import sys
import os
import time 

from typing import List
from uuid import uuid4
import RPi.GPIO as GPIO

import src.interfaces.button as button_interface
import src.interfaces.mqtt as mqtt_interface
import src.interfaces.neopixel as neopixel_interface
import src.utils.constants as constants
import src.architecture.component as architecture
import src.utils.types as types

global_compliance_state: types.ComplianceState = types.ComplianceState(
    alb_sec_group_compliant = types.ServiceState(),
    cloud_trail_compliant = types.ServiceState(),
    asg_sec_group_compliant = types.ServiceState(),
    ec2_instance_2a_compliant = types.ServiceState(),
    ec2_instance_2b_compliant = types.ServiceState(),
    rds_db_compliant = types.ServiceState(),
    rds_sec_group_compliant = types.ServiceState(),
    s3_bucket_compliant = types.ServiceState()
)

def create_signal_handler(mqtt_client: mqtt_interface.MqttClientInterface):
    """ Wrapper to provide signal_handler with references to objects needed to be shut down. """
    def signal_handler(sig, frame):
        """ Called when Ctl + C is pressed """
        mqtt_client.cleanup()
        GPIO.cleanup()
        sys.exit(0)
    return signal_handler

def on_button_clicked_callback():
    # TODO: Add timeout after button pressed - only allow every 30 seconds
    print("Pressed button")
    mqtt_client.publish_message(
        constants.MQTT_CLIENT_PUBLISHING_TOPIC,
        constants.MQTT_CLIENT_PUBLISHING_MESSAGE)

button_client: button_interface.ButtonInterface = button_interface.ButtonInterface(
    constants.BUTTON_PORT, 
    on_button_clicked_callback)

mqtt_client_options: types.MqttClientOption = types.MqttClientOption(
    endpoint=constants.MQTT_CLIENT_ENDPOINT,
    port=constants.MQTT_CLIENT_PORT,
    cert_filepath=constants.MQTT_CLIENT_CERT_FILEPATH,
    pri_key_filepath=constants.MQTT_CLIENT_PRI_KEY_FILEPATH,
    client_id=constants.MQTT_CLIENT_CLIENT_ID)

mqtt_client: mqtt_interface.MqttClientInterface = mqtt_interface.MqttClientInterface(
    global_compliance_state,
    mqtt_client_options,
    constants.MQTT_CLIENT_SUBSCRIPTION_TOPIC)

signal.signal(signal.SIGINT, create_signal_handler(mqtt_client))
signal.pause()

neopixel_client : neopixel_interface.NeopixelInterface = neopixel_interface.NeopixelInterface(
    port=constants.NEOPIXEL_PORT,
    nb_pixels=constants.NEOPIXEL_NB_PIXELS)

# TODO: Set up all of the connections and components
test_architecture_component: architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("alb_sec_group_compliant", [5, 6])],
    #component_connections=[],
    ingoing_connections=[types.ConnectionComponent("cloud_trail_compliant", [0, 1, 2, 3, 4])],
    outgoing_connections=[types.ConnectionComponent("rds_sec_group_compliant", [7, 8, 9, 10])]
    #outgoing_connections=[]
)

test_architecture_component2: architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("alb_sec_group_compliant", [24, 25])],
    #component_connections=[],
    ingoing_connections=[types.ConnectionComponent("cloud_trail_compliant", [17, 18, 19, 20, 21, 22, 23])],
    outgoing_connections=[types.ConnectionComponent("rds_sec_group_compliant", [26, 27, 28, 29, 30])]
    #outgoing_connections=[]
)

while True:
    test_architecture_component.update(global_compliance_state)
    #test_architecture_component2.update(global_compliance_state)
    neopixel_client.show_changes()