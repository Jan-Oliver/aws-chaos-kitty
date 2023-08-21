import os
import threading
import json

from dataclasses import dataclass
from concurrent.futures import Future
from typing import Callable

from awsiot import mqtt5_client_builder
from awscrt import mqtt5

from src.main import ComplianceState
import src.utils.constants as constants 
@dataclass
class MqttClientOptionType:
    """Configuration for the creation of MQTT5 client
    Account - Frankfurt - IoT Core - Mqtt test client - Raspi4 - Certificates (policy haengt am certificate) - iot receive anpassen bei anderem topic & publish -
    test client - subscribe auf broker - topic # - testen ob publish klappt -  
    Args:
        endpoint (str): Host name of AWS IoT server.
        port (int): Connection port for direct connection. "AWS IoT supports 443 and 8883.
        cert_filepath (str): Path to certificate file.
        pri_key_filepath (str): Path to private key file.
        client_id (str): Globally unique client id.
    """
    endpoint: str
    port: int
    cert_filepath: str
    pri_key_filepath: str
    client_id: str

class MqttClientInterface():
    # TODO: Add types to update state callback
    def __init__(self, global_compliance_state: ComplianceState, client_options: MqttClientOptionType, subscription_topic: str):
        """
        global_compliance_state (ComplianceState): Global compliance state of the architecture
        client_options (MqttClientOptionType): Configuration for the creation of MQTT5 client
        message_topic (str): Filter mask for topics to subscribe to, e.g. "test/topic"
        """
        self.global_compliance_state = global_compliance_state
        self.subscription_topic = subscription_topic
        self.timeout = 100
        self.future_stopped = Future()
        self.future_connection_success = Future()

        # Create MQTT5 client
        self.client: mqtt5.Client = mqtt5_client_builder.mtls_from_path(
            endpoint=client_options.endpoint,
            port=client_options.port,
            cert_filepath=client_options.cert_filepath,
            pri_key_filepath=client_options.ca_filepath,
            ca_filepath=client_options.ca_filepath,
            client_id=client_options.client_id,
            on_publish_received=self._on_publish_received,
            on_lifecycle_stopped=self._on_lifecycle_stopped,
            on_lifecycle_connection_success=self._on_lifecycle_connection_success,
            on_lifecycle_connection_failure=self._on_lifecycle_connection_failure
        )
        print("MQTT5 Client Created")

        print(f"Connecting to {client_options.endpoint} with client ID '{client_options.client_id}'...")
        self.client.start()

        # Wait for connection to be successful
        lifecycle_connect_success_data = self.future_connection_success.result(self.timeout)
        connack_packet = lifecycle_connect_success_data.connack_packet
        negotiated_settings = lifecycle_connect_success_data.negotiated_settings
        print(f"Connected to endpoint: {client_options.endpoint} with client ID '{client_options.client_id}' with reason_code:{repr(connack_packet.reason_code)}")

        # Subscribe to the topic
        print(f"Subscribing to topic '{self.subscription_topic}'...")
        subscribe_future = self.client.subscribe(subscribe_packet=mqtt5.SubscribePacket(
            subscriptions=[mqtt5.Subscription(
                topic_filter=self.subscription_topic,
                qos=mqtt5.QoS.AT_LEAST_ONCE)]
        ))
        suback = subscribe_future.result(self.timeout)
        print("Subscribed with {}".format(suback.reason_codes))
        
    # Callback for the lifecycle event Connection Success
    def _on_lifecycle_connection_success(self, lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
        print("Lifecycle Connection Success")
        self.future_connection_success.set_result(lifecycle_connect_success_data)

    # Callback for the lifecycle event Connection Failure
    def _on_lifecycle_connection_failure(self, lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
        print("Lifecycle Connection Failure")
        print(f"Connection failed with exception: {lifecycle_connection_failure.exception}")
    
    # Callback when any publish is received
    def _on_publish_received(self, publish_packet_data):
        publish_packet = publish_packet_data.publish_packet
        assert isinstance(publish_packet, mqtt5.PublishPacket)
        print(f"Received message from topic {publish_packet.topic}:{publish_packet.payload}")
        
        # TODO: Make this conversion safe/work
        # Message is /aws/bulb/<id>
        architecture_component_id = int(publish_packet.topic.split('/')[-1])
        acrchitecture_component_name = constants.MQTT_ID_TO_STATE_MAPPING.get(architecture_component_id)

        is_architecture_component_compliant = False
        if publish_packet.payload == constants.MQTT_CLIENT_SUBSCRIPTION_PAYLOAD_COMPLIANT:
            is_architecture_component_compliant = True

        if acrchitecture_component_name:
            setattr(self.global_compliance_state, acrchitecture_component_name, is_architecture_component_compliant)


    # Callback for the lifecycle event Stopped
    def _on_lifecycle_stopped(self, lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
        print("Lifecycle Stopped")
        self.future_stopped.set_result(lifecycle_stopped_data)


    def cleanup(self):
        """ Remove subscription and stop the client """
        print(f"Unsubscribing from topic {self.subscription_topic}")
        unsubscribe_future = self.client.unsubscribe(unsubscribe_packet=mqtt5.UnsubscribePacket(
            topic_filters=[self.subscription_topic]))
        unsuback = unsubscribe_future.result(self.timeout)
        print(f"Unsubscribed from topic {self.subscription_topic} with {unsuback.reason_codes}")
        print("Stopping Client")
        self.client.stop()
        self.future_stopped.result(self.timeout)
        print("Client Stopped!")

    def publish_message(self, topic: str, message: str):
        print(f"Publishing message to topic '{topic}': {message}")
        publish_future = self.client.publish(mqtt5.PublishPacket(
            topic=topic,
            payload=json.dumps(message),
            qos=mqtt5.QoS.AT_LEAST_ONCE
        ))
        publish_completion_data = publish_future.result(self.timeout)
        print(f"PubAck received with {repr(publish_completion_data.puback.reason_code)}")