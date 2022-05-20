import cv2
import numpy as np
import time
from PIL import Image, ImageDraw 
from controls import Controls

cap = cv2.VideoCapture("http://192.168.1.5:8081/video")

area_thresh = 450
isGreen = False

countdown_limit = 3
countdown = countdown_limit

elpsed_frametime = 0

PI = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPI_SPEED_MHZ = 90

image = Image.new("RGB", (240, 240), (255, 0, 255))
controls = Controls()

controls.newControl("hue", 0, 255, 65)

if PI == True:
    import RPi.GPIO as GPIO
    from ST7789 import ST7789
    from picamera.array import PiRGBArray
    from picamera import PiCamera

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
    
hue = 70

while True:
    t1 = time.time()

    ret, img = cap.read()
    output = np.zeros((400, 400, 3), dtype=np.uint8)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue = controls.getValues()['hue']
    lower_green = np.array([int(hue), 50, 50])
    upper_green = np.array([int(hue)+20, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 2)

    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    max_area = 0
    max_area_contour = -1
    
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if max_area <  area:
            max_area = area
            max_area_contour = i

        cv2.drawContours(res, [contour], 0, (0,255,133), 2)

    angle = ((countdown_limit - countdown)/countdown_limit)*360

    print(max_area)
    draw_half_circle_rounded(output, angle)        

    cv2.imshow("masked", res)
    cv2.imshow("output", output)
    cv2.imshow("input", img)

    key = cv2.waitKey(10)

    t2 = time.time()

    elpsed_frametime = (t2 - t1)
 
    if max_area > area_thresh:
        countdown = max(countdown - elpsed_frametime, 0)
        isGreen = True
    else:
        countdown = min(countdown + elpsed_frametime, 3)
        isGreen = False
     

