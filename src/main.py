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
    rds_sec_group_compliant = types.ServiceState(False),
    s3_bucket_compliant = types.ServiceState(False)
)

def create_signal_handler(
        mqtt_client: mqtt_interface.MqttClientInterface, 
        neopixel_client : neopixel_interface.NeopixelInterface):
    """ Wrapper to provide signal_handler with references to objects needed to be shut down. """
    def signal_handler(sig, frame):
        """ Called when Ctl + C is pressed """
        mqtt_client.cleanup()
        neopixel_client.cleanup()
        GPIO.cleanup()
        sys.exit(0)
    return signal_handler

last_click_timestamp = 0  # initializing the timestamp at the start
def on_button_clicked_callback(value):
    global last_click_timestamp

    current_time = time.time()
    
    # Check if the difference between the current time and the last click timestamp is more than 10 seconds
    if current_time - last_click_timestamp >= 10:
        print("Pressed button")
        mqtt_client.publish_message(
            constants.MQTT_CLIENT_PUBLISHING_TOPIC,
            constants.MQTT_CLIENT_PUBLISHING_MESSAGE)
        
        # Update the timestamp
        last_click_timestamp = current_time
    else:
        print("Button pressed too quickly. Please wait for 10 seconds between presses.")

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

neopixel_client : neopixel_interface.NeopixelInterface = neopixel_interface.NeopixelInterface(
    port=constants.NEOPIXEL_PORT,
    nb_pixels=constants.NEOPIXEL_NB_PIXELS)

# TODO: Set up all of the connections and components

# It is possible to have not outgoing/ingoing/component connections by specifing an empty list
example_architecture_component: architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("rds_db_compliant", [5, 6])],
    ingoing_connections=[types.ConnectionComponent("alb_sec_group_compliant", [0, 1, 2, 3, 4])],
    outgoing_connections=[]
)

# It is possible to have multiple outgoing/ingoing/component connections by specifing multiple ConnectionComponents in the list
example2_architecture_component2: architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("s3_bucket_compliant", [24, 25])],
    ingoing_connections=[types.ConnectionComponent("cloud_trail_compliant", [17, 18, 19, 20, 21, 22, 23])],
    outgoing_connections=[
        types.ConnectionComponent("asg_sec_group_compliant", [26, 27, 28, 29, 30]),
        types.ConnectionComponent("rds_sec_group_compliant", [7, 8, 9, 10])
        ]
)

architecture_components: List[architecture.ArchitectureComponent] = [
    example_architecture_component,
    example2_architecture_component2
]

signal.signal(signal.SIGINT, create_signal_handler(mqtt_client, neopixel_client))

while True:
    for architecture_component in architecture_components:
        architecture_component.update(global_compliance_state)

    neopixel_client.show_changes()