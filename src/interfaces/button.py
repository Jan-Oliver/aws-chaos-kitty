import RPi.GPIO as GPIO
from typing import Callable
    
class ButtonInterface():
    def __init__(self, port: int, callback: Callable[[], None]) -> None:
        self.BUTTON_GPIO = port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.BUTTON_GPIO, GPIO.FALLING, callback=callback, bouncetime=100)

