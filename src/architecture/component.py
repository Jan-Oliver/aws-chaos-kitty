from typing import List, Optional
from dataclasses import dataclass

from src.interfaces.neopixel import NeopixelInterface
from src.main import ComplianceState, ServiceState

@dataclass
class ConnectionType:
    state_id: str
    pixels: List[int]

class ArchitectureComponent():
    def __init__(self, 
                 neopixel_client: NeopixelInterface, 
                 component_connections: Optional[List[ConnectionType]], 
                 ingoing_connections: Optional[List[ConnectionType]], 
                 outgoing_connections: Optional[List[ConnectionType]]):
        
        self.neopixel_client = neopixel_client
        self.component_connections = component_connections
        self.ingoing_connections = ingoing_connections
        self.outgoing_connections = outgoing_connections

    def _update_ingoing_connections(self, global_compliance_state: ComplianceState):
        if not self.ingoing_connections:
            return
        
        for ingoing_connection in self.ingoing_connections:
            state_id = ingoing_connection.state_id
            pixels = ingoing_connection.pixels
            compliance_state = getattr(global_compliance_state, state_id)
            self.neopixel_client.update_connection_pixels(pixels, compliance_state)

    def _update_outgoing_connections(self, global_compliance_state: ComplianceState):
        if not self.outgoing_connections:
                return
            
        for outgoing_connection in self.outgoing_connections:
            state_id = outgoing_connection.state_id
            pixels = outgoing_connection.pixels
            compliance_state = getattr(global_compliance_state, state_id)
            self.neopixel_client.update_connection_pixels(pixels, compliance_state)

    def _update_component_connections(self, global_compliance_state: ComplianceState):
        if not self.component_connections:
                return
            
        for component_connection in self.component_connections:
            state_id = component_connection.state_id
            pixels = component_connection.pixels
            compliance_state = getattr(global_compliance_state, state_id)
            self.neopixel_client.update_component_pixels(pixels, compliance_state)

    def update(self, global_compliance_state: ComplianceState):
        self._update_ingoing_connections(global_compliance_state)
        self._update_outgoing_connections(global_compliance_state)
        self._update_component_connections(global_compliance_state)
