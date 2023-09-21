from enum import Enum
from dataclasses import dataclass
from typing import List


@dataclass
class ServiceState:
    COMPLIANT: bool = True

    
@dataclass
class ComplianceState:
    """ Defines compliance state globally - Singleton """
    # Not yet part of experiment
    igw_compliant: ServiceState
    # Non-Compliant: Open Application Load Balancer Security Group
    alb_sec_group_compliant: ServiceState
    # Not yet part of experiment
    alb_compliant: ServiceState
    # Non-Compliant: Cloud Trail Turned off
    cloud_trail_compliant: ServiceState
    # Non-Compliant: Open Auto Scaling Group Security Group
    asg_sec_group_compliant: ServiceState
    # Non-Compliant: Unsafe Role for EC2 Instance in AZ A
    ec2_instance_2a_compliant: ServiceState
    # Not yet part of experiment
    ec2_instance_2a_sec_group: ServiceState
    # Non-Compliant: Unsafe Role for EC2 Instance in AZ B
    ec2_instance_2b_compliant: ServiceState
    # Not yet part of experiment
    ec2_instance_2b_sec_group: ServiceState
    # Non-Compliant: Change Relational Database System Authentication
    rds_db_compliant: ServiceState
    # Non-Compliant: Open Relational Database System Security Group
    rds_sec_group_compliant: ServiceState
    # Not yet part of experiment
    rds_replication_compliant: ServiceState
    # Non-Compliant: S3 Bucket public
    s3_bucket_compliant: ServiceState
    # Helper connection that is not used for any specific state
    general_connection: ServiceState

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(ComplianceState, cls).__new__(cls)
        return cls._instance

@dataclass
class ConnectionComponent:
    state_id: str
    pixels: List[int]


@dataclass
class MqttClientOption:
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