from picamera import PiCamera
import RPi.GPIO as GPIO

PIN = 14
FORMAT = 'jpeg'
RESOLUTION = (1024, 768)

class Raspberry:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = RESOLUTION
        self.camera.start_preview()
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(PIN, GPIO.IN)

    def Muvement(self):
        return self.GPIO.input(PIN)

    def Capture(self,stream):
        return self.camera.capture(stream, FORMAT)