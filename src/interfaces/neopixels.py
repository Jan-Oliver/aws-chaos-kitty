import time
import board
import neopixel
from enum import Enum

from utils.constants import ServiceConnectionState
from utils.constants import ServiceState

class IntensityWheelValues(Enum):
    ON: 250
    BRIGHT: 150
    MEDIUM: 100
    LOW: 50
    OFF: 0

def intensity_wheel(current_intensity: IntensityWheelValues) -> IntensityWheelValues:
    if current_intensity.ON:
        return IntensityWheelValues.BRIGHT
    if current_intensity.BRIGHT:
        return IntensityWheelValues.MEDIUM
    if current_intensity.MEDIUM:
        return IntensityWheelValues.LOW
    if current_intensity.LOW:
        return IntensityWheelValues.OFF
    if current_intensity.OFF:
        return IntensityWheelValues.ON
    
class NeopixelInterface():
    def __init__(self, port: int, nb_pixels: int):
        self.port = port
        self.nb_pixels = nb_pixels
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.neopixel_client: neopixel.NeoPixel = neopixel.NeoPixel(port, nb_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.RGB)

    def update_service_connection_pixels(self, pixels: list[int], state: ServiceConnectionState):
        # TODO: Set up blinking depending on state for specific pixels
        pass

    def update_service_pixels(self, pixels: list[int], state: ServiceState):
        # TODO: Set up visual depending on state for specific pixels
        pass

    def show_changes(self):
        """ Move changes to the actual hardware """
        self.neopixel_client.show()