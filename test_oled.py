import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

print("Turning on OLED...")
device.contrast(255)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 10), "HELLO", fill="white")
    draw.text((10, 30), "IT WORKS", fill="white")

print("Done - check screen")
time.sleep(10)
