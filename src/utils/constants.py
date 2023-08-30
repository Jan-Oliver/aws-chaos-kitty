import os
from uuid import uuid4
import board

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
CERTIFICATES_PATH = os.path.join(DIR_PATH, "certificates")

# Port for the button to start the game
BUTTON_PORT = 16

# Port for Neopixel LED stripe
NEOPIXEL_PORT = board.D18
NEOPIXEL_NB_PIXELS = 100

# Mqtt client config
MQTT_CLIENT_ENDPOINT = "a2f97hrgv6egz9-ats.iot.eu-central-1.amazonaws.com"
MQTT_CLIENT_PORT = 8883
MQTT_CLIENT_CERT_FILEPATH = os.path.join(CERTIFICATES_PATH, "4cd4ee53ab6b0dff22c32f9acaa08221ad1dd4d58dbb34ba889b6a7f77b2b6d0-certificate.pem.crt")
MQTT_CLIENT_PRI_KEY_FILEPATH = os.path.join(CERTIFICATES_PATH, "4cd4ee53ab6b0dff22c32f9acaa08221ad1dd4d58dbb34ba889b6a7f77b2b6d0-private.pem.key")
MQTT_CLIENT_CLIENT_ID = f"Raspi4"

# Mqtt publish topic
MQTT_CLIENT_PUBLISHING_TOPIC = "test/topic"
MQTT_CLIENT_PUBLISHING_MESSAGE = ""

# Mqtt subscription topic, + is a level 1 wildcard in mqtt
MQTT_CLIENT_SUBSCRIPTION_TOPIC = "aws/bulb/+"
MQTT_CLIENT_SUBSCRIPTION_PAYLOAD_COMPLIANT = 'green'

# Mapping of ID of iot core messaging to aws architecture
MQTT_ID_TO_STATE_MAPPING = {
    31: "alb_sec_group_compliant",
    32: "cloud_trail_compliant",
    33: "asg_sec_group_compliant",
    34: "ec2_instance_2a_compliant",
    35: "ec2_instance_2b_compliant",
    36: "rds_db_compliant",
    37: "rds_sec_group_compliant",
    38: "s3_bucket_compliant",
}