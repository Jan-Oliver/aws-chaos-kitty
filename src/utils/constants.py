import os
from uuid import uuid4
import board

# Port for the button to start the game
BUTTON_PORT = 16

# Port for Neopixel LED stripe
NEOPIXEL_PORT = board.D18
NEOPIXEL_NB_PIXELS = 300

# Mqtt client config
MQTT_CLIENT_ENDPOINT = "TODO",
MQTT_CLIENT_PORT = 8883,
MQTT_CLIENT_CERT_FILEPATH = os.path.join('todo'),
MQTT_CLIENT_PRI_KEY_FILEPATH = os.path.join('todo'),
MQTT_CLIENT_CLIENT_ID = f"chaos-kitty-raspi-{uuid4()}"

# Mqtt publish topic
MQTT_CLIENT_PUBLISHING_TOPIC = "TODO"
MQTT_CLIENT_PUBLISHING_MESSAGE = ""

# Mqtt subscription topic
MQTT_CLIENT_SUBSCRIPTION_TOPIC = "aws/bulb/"
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