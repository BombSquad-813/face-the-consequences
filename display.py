import sys
sys.path.insert(0, '/home/pi/.local/lib/python3.13/site-packages')
import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from rpi_ws281x import PixelStrip, Color

RELAY_PIN = 17
BUZZER_PIN = 12
LED_GREEN = 16
LED_RED = 20
NEO_PIN = 18
NEO_COUNT = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
device.contrast(255)

strip = PixelStrip(NEO_COUNT, NEO_PIN, 800000, 5, False, 255, 0)
strip.begin()

class Display:
    def ring_green(self):
        for i in range(NEO_COUNT):
            strip.setPixelColor(i, Color(0, 150, 50))
        strip.show()

    def ring_red(self):
        for i in range(NEO_COUNT):
            strip.setPixelColor(i, Color(255, 0, 0))
        strip.show()

    def ring_off(self):
        for i in range(NEO_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

    def show_ready(self):
        with canvas(device) as d:
            d.text((5, 0), "SENTINEL GATE", fill="white")
            d.text((5, 14), "--------------", fill="white")
            d.text((5, 28), "ARMED", fill="white")
            d.text((5, 42), "Scan badge+face", fill="white")
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_RED, GPIO.LOW)
        self.ring_off()

    def show_granted(self, name=""):
        with canvas(device) as d:
            d.text((5, 0), "ACCESS GRANTED", fill="white")
            d.text((5, 20), "Hi " + name[:12], fill="white")
            d.text((5, 40), "Door unlocked", fill="white")
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_RED, GPIO.LOW)
        self.ring_green()

    def show_denied(self, reason=""):
        with canvas(device) as d:
            d.text((5, 0), "ACCESS DENIED", fill="white")
            d.text((5, 20), reason, fill="white")
            d.text((5, 40), "BLOCKED", fill="white")
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.HIGH)
        self.ring_red()

    def buzz_alert(self):
        pwm = GPIO.PWM(BUZZER_PIN, 2000)
        pwm.start(90)
        time.sleep(2)
        pwm.stop()

    def unlock_door(self):
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(3)
        GPIO.output(RELAY_PIN, GPIO.HIGH)
