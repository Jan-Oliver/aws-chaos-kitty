import time
import neopixel
from enum import Enum

import src.utils.types as types

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

    def update_connection_pixels(self, pixels: list[int], compliance_state: types.ServiceState):
        base_color = (255, 255, 255) if compliance_state.COMPLIANT else (0, 255, 0)  # white for compliant, red for non-compliant
        intensity_values = [intensity.value for intensity in IntensityWheelValues]

        for idx, pixel in enumerate(pixels):
            # Create a moving effect using the intensity wheel and time
            # Add idx to make it "move" in the other direction
            intensity_factor = intensity_values[int((time.time() * 2 - idx) % len(intensity_values))] / 255.0  # multipled time with 2 to speed up movement
            adjusted_color = tuple(int(value * intensity_factor) for value in base_color)
            self.neopixel_client[pixel] = adjusted_color

    def update_component_pixels(self, pixels: list[int], compliance_state: types.ServiceState):
        color = (255, 0, 0) if compliance_state.COMPLIANT else (0, 255, 0)  # white for compliant, red for non-compliant
        for pixel in pixels:
            self.neopixel_client[pixel] = color

    def show_changes(self):
        """ Move changes to the actual hardware """
        self.neopixel_client.show()