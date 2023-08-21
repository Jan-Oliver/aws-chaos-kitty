from abc import ABC, abstractmethod
from typing import List, Optional

from src.interfaces.neopixels import NeopixelInterface


class AbstractArchitectureComponent(ABC):
    def __init__(self, 
                 neopixels_client: NeopixelInterface, 
                 component_connections: List[int], 
                 ingoing_connections: Optional[List[int]], 
                 outgoing_connections: Optional[List[int]]):
        
        self.neopixels_client = neopixels_client
        self.component_connections = component_connections
        self.ingoing_connections = ingoing_connections
        self.outgoing_connections = outgoing_connections

    def _update_ingoing_connections(self):
        pass

    def _update_outgoing_connections(self):
        pass

    def _update_component_connections(self):
        pass

    @abstractmethod
    def update(self):
        pass