import time
import neopixel
import random
import math
from enum import Enum

import src.utils.types as types

class IntensityWheelValues(Enum):
    ON = 250
    BRIGHT = 70
    MEDIUM = 25
    LOW13 = 13
    LOW12 = 12
    LOW11 = 11
    LOW10 = 10
    LOW9 = 9
    LOW8 = 8
    LOW7 = 7
    LOW6 = 6
    LOW5 = 5
    LOW4 = 4
    LOW3 = 3
    LOW = 2
    OFF = 1
    OFF2 = 0
    
class NeopixelInterface():
    def __init__(self, port: int, nb_pixels: int):
        self.port = port
        self.nb_pixels = nb_pixels
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.neopixel_client: neopixel.NeoPixel = neopixel.NeoPixel(port, nb_pixels, brightness=1, auto_write=False, pixel_order=neopixel.RGB)
        self.int_values = [intensity.value * 0.05 for intensity in IntensityWheelValues] 
        self.len_int_values = len(self.int_values)
        self.max_pulse_value = 255
        self.min_pulse_value = 50
        self.current_cycle_step = 0
        self.cycle_length = 100
        self.amplitude = (self.max_pulse_value - self.min_pulse_value) / 2
        self.offset = (self.max_pulse_value + self.min_pulse_value) / 2
        self.current_intensity = int(self.amplitude * math.sin(2 * math.pi * self.current_cycle_step / self.cycle_length) + self.offset)


    def update_connection_pixels(self, pixels: list[int], compliance_state: types.ServiceState):
        base_color = (255, 255, 255) if compliance_state.COMPLIANT else (100, 255, 0)  # white for compliant, red for non-compliant
        c_time = time.time()
        for idx, pixel in enumerate(pixels):
            # Create a moving effect using the intensity wheel and time
            # Add idx to make it "move" in the other direction
            intensity_factor = self.int_values[int((c_time * 10 - idx) % self.len_int_values)] / 255.0  # multipled time with 2 to speed up movement
            adjusted_color = tuple(int(value * intensity_factor) for value in base_color)
            self.neopixel_client[pixel] = adjusted_color

    def update_sec_group_pixels(self, pixels: list[int], compliance_state: types.ServiceState):
        base_color = (0, 0, 255) if compliance_state.COMPLIANT else (0, 255, 0)  # white for compliant, red for non-compliant

        if not compliance_state.COMPLIANT:
            base_color = (base_color[0] * self.current_intensity / 255, base_color[1] * self.current_intensity / 255, base_color[2] * self.current_intensity / 255 )
        
        for idx, pixel in enumerate(pixels):
            self.neopixel_client[pixel] = base_color

    def update_component_pixels(self, pixels: list[int], compliance_state: types.ServiceState):
        base_color = (255, 0, 0) if compliance_state.COMPLIANT else (0, 255, 0)  # white for compliant, red for non-compliant

        if not compliance_state.COMPLIANT:
            base_color = (base_color[0] * self.current_intensity / 255, base_color[1] * self.current_intensity / 255, base_color[2] * self.current_intensity / 255 )
        
        for pixel in pixels:
            self.neopixel_client[pixel] = base_color

    def show_changes(self):
        """ Move changes to the actual hardware """
        self.neopixel_client.show()
        self.current_cycle_step = self.current_cycle_step + 1
        if self.current_cycle_step == self.cycle_length - 1:
            self.current_cycle_step = 0
        self.current_intensity = int(self.amplitude * math.sin(2 * math.pi * self.current_cycle_step / self.cycle_length) + self.offset)

    def cleanup(self):
        """ Celan up """
        self.neopixel_client.deinit()
