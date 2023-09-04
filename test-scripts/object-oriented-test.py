from enum import Enum
import time
import neopixel
import types  # Make sure to import this if you use types.ServiceState

class ColorWheelValues(Enum):
    ON = (255, 255, 255)  # white
    BRIGHT = (250, 250, 250)
    MEDIUM = (128, 128, 128)
    LOW = (70, 70, 70)
    OFF = (10, 10, 10)
    OFF2 = (0, 0, 0)  # black

class NeopixelInterface():
    def __init__(self, port: int, nb_pixels: int):
        self.port = port
        self.nb_pixels = nb_pixels
        self.neopixel_client: neopixel.NeoPixel = neopixel.NeoPixel(
            port, nb_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.RGB)
        
        self.color_wheel_values = [color.value for color in ColorWheelValues]

    def update_connection_pixels(self, pixels: list[int], compliance_state: types.ServiceState):
        base_color = (255, 255, 255) if compliance_state.COMPLIANT else (100, 255, 0)

        for idx, pixel in enumerate(pixels):
            # Use the color wheel to determine pixel color
            color_index = int((time.time() * 2 - idx) % len(self.color_wheel_values))
            self.neopixel_client[pixel] = self.multiply_colors(base_color, self.color_wheel_values[color_index])

    def multiply_colors(self, color1: tuple, color2: tuple) -> tuple:
        return tuple(int(a * b / 255) for a, b in zip(color1, color2))

# Usage
interface = NeopixelInterface(port=0, nb_pixels=10)
pixels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
state = types.ServiceState.COMPLIANT  # or whatever your real state value is
interface.update_connection_pixels(pixels, state)
