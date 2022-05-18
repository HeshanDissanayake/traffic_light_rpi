import cv2
import numpy as np

buffer = np.zeros((240, 240, 3), dtype=np.uint8)

def draw_half_circle_rounded(image, angle):
    height, width = image.shape[0:2]
    radius = 100
    center = (width // 2, height // 2)
    axes = (radius, radius)
    startAngle = -90
    thickness = 10
    
    cv2.ellipse(image, center, axes, 0, startAngle, angle-90, (80,255,0), thickness)
    

angle = 0
increment = 1
while True:
    buffer = np.zeros((240, 240, 3), dtype=np.uint8)
    angle = angle + increment

    if angle > 360:
        increment = -1
    
    if angle < 0:
        increment = 1
    
    
    draw_half_circle_rounded(buffer, angle)
    cv2.imshow("buffer", buffer)
    cv2.waitKey(10)

