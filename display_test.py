#!/usr/bin/env python

import time
import math
import cv2
import RPi.GPIO as GPIO
from ST7789 import ST7789
from PIL import Image, ImageDraw
import numpy as np

SPI_SPEED_MHZ = 90

# Give us an image buffer to draw into
image = Image.new("RGB", (240, 240), (255, 0, 255))

# Standard display setup for Pirate Audio, except we omit the backlight pin
st7789 = ST7789(
    rotation=90,     # Needed to display the right way up on Pirate Audio
    port=0,          # SPI port
    cs=1,            # SPI port Chip-select channel
    dc=9,            # BCM pin used for data/command
    backlight=None,  # We'll control the backlight ourselves
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000
)

GPIO.setmode(GPIO.BCM)

# We must set the backlight pin up as an output first
GPIO.setup(13, GPIO.OUT)

# Set up our pin as a PWM output at 500Hz
backlight = GPIO.PWM(13, 500)

# Start the PWM at 100% duty cycle
backlight.start(100)

def draw_half_circle_rounded(image, angle):
    height, width = image.shape[0:2]
    radius = 100
    center = (width // 2, height // 2)
    axes = (radius, radius)
    startAngle = -90
    thickness = 10
    
    cv2.ellipse(image, center, axes, 0, startAngle, angle-90, (80,255,0), thickness)
    

while True:
   
    brightness = ((math.sin(time.time()) + 1) / 2.0) * 100
    backlight.ChangeDutyCycle(brightness)

    buffer = np.zeros((240, 240, 3), dtype=np.uint8)
    angle = angle + increment

    if angle > 360:
        increment = -1
    
    if angle < 0:
        increment = 1
    
    
    draw_half_circle_rounded(buffer, angle)

    color_coverted = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)
  
    image = Image.fromarray(color_coverted)
    
    # Display the resulting image
    st7789.display(image)
    time.sleep(1.0 / 30)

backlight.stop()
