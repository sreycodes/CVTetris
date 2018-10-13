import random, pygame, sys
from pygame.locals import *
import numpy as np
import cv2
import imutils
import time
from collections import deque
from datetime import datetime


cap = cv2.VideoCapture(0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=12)
direction = "ND"
height = 320
width = 600

def remove_from_array(base_array, test_array):
    for index in range(len(base_array)):
        if np.array_equal(base_array[index], test_array):
            base_array.pop(index)
            break
    # raise ValueError('remove_from_array(array, x): x not in array')

def find_move(coords):
    '''Calculates the direction of motion

        Arguments: Two center variables used to determine direction of motion

        Returns: A string specifying the direction of motion'''
    # check if translation in x or y direction
    print(coords)
    if(len(coords) == 0):
        return "NONE"
    elif(coords[0] < width / 4):
        return "LEFT"
    elif(coords[0] > 3 * width / 4):
        return "RIGHT"
    elif(coords[1] > 3 * height / 4):
        return "DOWN"
    elif(coords[1] < height / 4):
        return "UP"
    else:
        return "NONE"

while True:
    grabbed, frame = cap.read()
    frame = imutils.resize(frame, width=width, height=height)
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    radius = -1
    x, y = width / 2, height / 2
    radius2 = -1
    x2, y2 = width / 2, height / 2

    coords = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    center2 = None

    if len(coords) > 1:
        print(coords)
        circle_1 = max(coords, key=cv2.contourArea)
        print(circle_1)
        # coords = [x for x in coords if not (x==circle_1).all()]
        remove_from_array(coords, circle_1)
        print(coords)
        circle_2 = max(coords, key=cv2.contourArea)
        print(circle_2)
        ((x, y), radius) = cv2.minEnclosingCircle(circle_1)
        ((x2, y2), radius2) = cv2.minEnclosingCircle(circle_2)
        M = cv2.moments(circle_1)
        M2 = cv2.moments(circle_2)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))


    if radius > 10:
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

    if radius2 > 10:
        cv2.circle(frame, (int(x2), int(y2)), int(radius2), (0, 255, 255), 2)
        cv2.circle(frame, center2, 5, (0, 0, 255), -1)

    # print(pts)
    # if type(center) == tuple:
    #     pts.appendleft(center)
    # if len(pts) == 12:
    #     temp_direction = translation(pts[0], pts[len(pts) - 1])
    #     if direction != temp_direction:
    #         direction = temp_direction
    #     # else:
    #     #     direction = None
    # else:
    #     direction = "ND"
    # print(direction)
    time.sleep(0.2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("E"):
        break

cap.release()
cv2.destroyAllWindows()
