from io import BytesIO
from picamera import PiCamera
import RPi.GPIO as GPIO


class Raspberry:
    def __init__(self,config):
        self.pin = config['pin']
        self.format = config['format']
        self.resolution = (config['hight'],config['wight'])
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin, GPIO.IN)

    def Muvement(self):
        return self.GPIO.input(self.pin)

    def Capture(self):
         self.stream =BytesIO()
         with PiCamera() as self.camera:
             self.camera.resolution = self.resolution
             self.camera.start_preview()
             self.camera.capture(self.stream, self.format)
             self.camera.stop_preview()
             return self.stream.getbuffer()