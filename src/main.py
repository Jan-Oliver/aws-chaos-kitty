#!/usr/bin/env python3
from dataclasses import dataclass
import signal
import sys
import os
from uuid import uuid4
from enum import Enum
import RPi.GPIO as GPIO

import src.interfaces.button as button_interface
import src.interfaces.mqtt as mqtt_interface
import src.utils.constants as constants


class ServiceState(Enum):
    NON_COMPLIANT: 0
    COMPLIANT: 1

@dataclass
class ComplianceState:
    """ Defines compliance state globally - Singleton """
    # Non-Compliant: Open Application Load Balancer Security Group
    alb_sec_group_compliant: ServiceState
    # Non-Compliant: Cloud Trail Turned off
    cloud_trail_compliant: ServiceState
    # Non-Compliant: Open Auto Scaling Group Security Group
    asg_sec_group_compliant: ServiceState
    # Non-Compliant: Unsafe Role for EC2 Instance in AZ A
    ec2_instance_2a_compliant: ServiceState
    # Non-Compliant: Unsafe Role for EC2 Instance in AZ B
    ec2_instance_2b_compliant: ServiceState
    # Non-Compliant: Change Relational Database System Authentication
    rds_db_compliant: ServiceState
    # Non-Compliant: Open Relational Database System Security Group
    rds_sec_group_compliant: ServiceState
    # Non-Compliant: S3 Bucket public
    s3_bucket_compliant: ServiceState

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(ComplianceState, cls).__new__(cls)
        return cls._instance

global_compliance_state: ComplianceState = ComplianceState(
    alb_sec_group_compliant = ServiceState.COMPLIANT,
    cloud_trail_compliant = ServiceState.COMPLIANT,
    asg_sec_group_compliant = ServiceState.COMPLIANT,
    ec2_instance_2a_compliant = ServiceState.COMPLIANT,
    ec2_instance_2b_compliant = ServiceState.COMPLIANT,
    rds_db_compliant = ServiceState.COMPLIANT,
    rds_sec_group_compliant = ServiceState.COMPLIANT,
    s3_bucket_compliant = ServiceState.COMPLIANT,
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
    print("Pressed button")
    mqtt_client.publish_message(
        constants.MQTT_CLIENT_PUBLISHING_TOPIC,
        constants.MQTT_CLIENT_PUBLISHING_MESSAGE)

button_client: button_interface.ButtonInterface = button_interface.ButtonInterface(
    constants.BUTTON_PORT, 
    on_button_clicked_callback)

mqtt_client_options: mqtt_interface.MqttClientOptionType = mqtt_interface.MqttClientOptionType(
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

# TODO: Main loop -> 
while True:
    # TODO: Take the current state and update all of the architecture components
    pass

