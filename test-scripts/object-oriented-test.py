from enum import Enum
import time
import neopixel
import board

from enum import Enum
from dataclasses import dataclass
from typing import List


@dataclass
class ServiceState:
    COMPLIANT: bool = True

class IntensityWheelValues(Enum):
    ON = 250
    BRIGHT = 70
    MEDIUM = 25
    LOW = 2
    OFF = 1
    OFF2 = 0
    
class NeopixelInterface():
    def __init__(self, port: int, nb_pixels: int):
        self.port = port
        self.nb_pixels = nb_pixels
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.neopixel_client: neopixel.NeoPixel = neopixel.NeoPixel(port, nb_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.RGB)
        self.int_values = [intensity.value for intensity in IntensityWheelValues]
        self.len_int_values = len(self.int_values)


    def update_connection_pixels(self, pixels: list[int], compliance_state: ServiceState):
        base_color = (255, 255, 255) if compliance_state.COMPLIANT else (100, 255, 0)  # white for compliant, red for non-compliant
        c_time = time.time()
        for idx, pixel in enumerate(pixels):
            # Create a moving effect using the intensity wheel and time
            # Add idx to make it "move" in the other direction
            intensity_factor = self.int_values[int((c_time * 100 - idx) % self.len_int_values)] / 255.0  # multipled time with 2 to speed up movement
            adjusted_color = tuple(int(value * intensity_factor) for value in base_color)
            self.neopixel_client[pixel] = adjusted_color
        
        self.neopixel_client.show()
        
    def show_changes(self):
        self.neopixel_client.show()

# Port for Neopixel LED stripe
NEOPIXEL_PORT = board.D18
# Number of LED pixels used for Neopixel stripe
NEOPIXEL_NB_PIXELS = 10

# Usage
interface = NeopixelInterface(port=NEOPIXEL_PORT, nb_pixels=NEOPIXEL_NB_PIXELS)
pixels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
state = ServiceState(COMPLIANT=False)  # or whatever your real state value is
for i in range(100):
    interface.update_connection_pixels(pixels, state)
    time.sleep(0.01)

