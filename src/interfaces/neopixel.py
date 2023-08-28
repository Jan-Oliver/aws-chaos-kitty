import time
import board
import neopixel
from enum import Enum

from src.main import ServiceState

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

    def update_connection_pixels(self, pixels: list[int], compliance_state: ServiceState):
        base_color = (255, 255, 255) if compliance_state == ServiceState.COMPLIANT else (255, 0, 0)  # white for compliant, red for non-compliant
        intensity_values = [intensity.value for intensity in IntensityWheelValues]
        
        for idx, pixel in enumerate(pixels):
            # Create a moving effect using the intensity wheel and time
            intensity_factor = intensity_values[int((idx + time.time() * 2) % len(intensity_values))] / 255.0  # multipled time with 2 to speed up movement
            adjusted_color = tuple(int(value * intensity_factor) for value in base_color)
            self.neopixel_client[pixel] = adjusted_color

    def update_component_pixels(self, pixels: list[int], compliance_state: ServiceState):
        color = (255, 255, 255) if compliance_state == ServiceState.COMPLIANT else (255, 0, 0)  # white for compliant, red for non-compliant
        for pixel in pixels:
            self.neopixel_client[pixel] = color

    def show_changes(self):
        """ Move changes to the actual hardware """
        self.neopixel_client.show()