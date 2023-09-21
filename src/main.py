#!/usr/bin/env python3
import signal
import sys
import os
import time
import keyboard

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
    igw_compliant = types.ServiceState(), # Not yet part of experiment
    alb_sec_group_compliant = types.ServiceState(),
    alb_compliant = types.ServiceState(), # Not yet part of experiment
    cloud_trail_compliant = types.ServiceState(),
    asg_sec_group_compliant = types.ServiceState(),
    ec2_instance_2a_compliant = types.ServiceState(),
    ec2_instance_2a_sec_group = types.ServiceState(), # Not yet part of experiment
    ec2_instance_2b_compliant = types.ServiceState(),
    ec2_instance_2b_sec_group = types.ServiceState(), # Not yet part of experiment
    rds_db_compliant = types.ServiceState(),
    rds_sec_group_compliant = types.ServiceState(),
    rds_replication_compliant = types.ServiceState(), # Not yet part of experiment
    s3_bucket_compliant = types.ServiceState(),
    general_connection = types.ServiceState() # General connection that will not be updated by experiment
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

"""
A: 1, 2, 3, 100, 99, 98
B: 4-15 (RDS AZ1 <-> RDS AZ2)
C: 16, 17, 18, 19, 20, 112, 110
D: 35-21 (EC2 AZ1 -> RDS AZ2)
E: 36-39, 106 (EC2 AZ1)
F: 50-40 (ALB -> EC2 AZ1)
G: 51, 52, 53, 54, 69 (ALB)
H: 55, 54 (IGW -> ALB)
I: 56, 57, 58, 59 (IGW)
J: 60, 61, 62, 63 (Cloud Trail)
K: 64, 65, 66, 67 (S3)
L: 70-78 (ALB -> EC2 AZ2)
M: 79-84 (EC2 AZ2)
N: 85-97 (EC2 AZ2 -> RDS AZ1)
O: 105-101 (EC2 AZ1 -> RDS AZ1)
P: 107-110 (EC2 AZ2 -> RDS AZ2)
"""
# TODO: Set up all of the connections and components
s3_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("s3_bucket_compliant", [64, 65, 66, 67])],
    ingoing_connections=[],
    outgoing_connections=[],
)

cloudtrail_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("cloud_trail_compliant", [60, 61, 62, 63])],
    ingoing_connections=[],
    outgoing_connections=[],
)

igw_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("igw_compliant", [56, 57, 58, 59])],
    ingoing_connections=[],
    outgoing_connections=[types.ConnectionComponent("general_connection", [55, 54])],
)

alb_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("alb_compliant", [50, 51, 52, 53, 68])],
    ingoing_connections=[types.ConnectionComponent("alb_sec_group_compliant", [54])],
    outgoing_connections=[types.ConnectionComponent("general_connection", [49, 48, 47, 46, 45, 44, 43, 42, 41, 40]), # (ALB -> EC2 AZ1)
                          types.ConnectionComponent("general_connection", [69, 70, 71, 72, 73, 74, 75, 76, 77, 78 ])] # (ALB -> EC2 AZ2)
)

ec2_az1_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("ec2_instance_2a_compliant", [36, 37, 38, 39, 105, 106])],
    ingoing_connections=[types.ConnectionComponent("ec2_instance_2a_sec_group", [41, 40])],
    outgoing_connections=[types.ConnectionComponent("general_connection", [104, 103, 102, 101]), # (EC2 AZ1 -> RDS AZ1)
                          types.ConnectionComponent("general_connection", [35, 34, 33, 32, 31, 30, 29, 28, 27,26, 25, 24, 23, 22, 21])] # (EC2 AZ1 -> RDS AZ2)
)

ec2_az2_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("ec2_instance_2b_compliant", [79, 80, 81, 82, 83])],
    ingoing_connections=[types.ConnectionComponent("ec2_instance_2b_sec_group", [77, 78])],
    outgoing_connections=[types.ConnectionComponent("general_connection", [107, 108, 109, 110]), # (EC2 AZ2 -> RDS AZ2)
                          types.ConnectionComponent("general_connection", [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97])] # (EC2 AZ2 -> RDS AZ1)
)

rds_az1_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("rds_db_compliant", [1, 2, 3, 100, 99, 98])],
    ingoing_connections=[types.ConnectionComponent("rds_sec_group_compliant", [102, 101]),
                         types.ConnectionComponent("rds_sec_group_compliant", [96, 97])],       
    outgoing_connections=[types.ConnectionComponent("rds_replication_compliant", [4, 5, 6, 7, 8, 9, 10])]
)

rds_az2_component : architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("rds_db_compliant", [16, 17, 18, 19, 20, 112, 111])],
    ingoing_connections=[types.ConnectionComponent("rds_sec_group_compliant", [109, 110]),
                         types.ConnectionComponent("rds_sec_group_compliant", [22, 21])],
    outgoing_connections=[types.ConnectionComponent("rds_replication_compliant", [15, 14, 13, 12, 11, 10])]
)

# TODO: Fix this with global per Connection Component State or something. Per connection we can
# specify the behaviour we want
# Dirty hack to overwrite all of the connections when replication is off.
rds_no_replication_component: architecture.ArchitectureComponent = architecture.ArchitectureComponent(
    neopixel_client = neopixel_client,
    component_connections=[types.ConnectionComponent("rds_replication_compliant", [16, 17, 18, 19, 20, 112, 111])],
    ingoing_connections=[],
    outgoing_connections=[types.ConnectionComponent("rds_replication_compliant", [107, 108, 109, 110]),
                          types.ConnectionComponent("rds_replication_compliant", [35, 34, 33, 32, 31, 30, 29, 28, 27,26, 25, 24, 23, 22, 21])]
)

#
architecture_components: List[architecture.ArchitectureComponent] = [
    s3_component,
    cloudtrail_component,
    igw_component,
    alb_component,
    ec2_az1_component,
    ec2_az2_component,
    rds_az1_component,
    rds_az2_component,
    rds_no_replication_component,
]


signal.signal(signal.SIGINT, create_signal_handler(mqtt_client, neopixel_client))
signal.signal(signal.SIGTERM, create_signal_handler(mqtt_client, neopixel_client))

current_time = time.time()
while True:
    for architecture_component in architecture_components:
        architecture_component.update(global_compliance_state)
    neopixel_client.show_changes()

    if keyboard.is_pressed("ctrl") and keyboard.is_pressed("q"):
        print("Stopping script execution")
        os.kill(os.getpid(), signal.SIGTERM)
