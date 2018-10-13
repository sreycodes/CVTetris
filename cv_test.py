import numpy as np
import cv2
import imutils
from collections import deque


cap = cv2.VideoCapture(0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=12)
direction = "ND"


def translation(first_coord, second_coord):
    '''Calculates the direction of motion

        Arguments: Two center variables used to determine direction of motion

        Returns: A string specifying the direction of motion'''
    # check if translation in x or y direction
    delta_y = int(second_coord[1] - first_coord[1])
    delta_x = int(second_coord[0] - first_coord[0])
    if delta_x != 0:
        axis = abs(delta_y) / abs(delta_x)
    else:
        axis = 0

    if axis > 1:
        if delta_y > 0:
            return "Up"
        elif delta_y < 0:
            return "Down"
    elif axis < 1:
        if delta_x > 0:
            return "Left"
        elif delta_x < 0:
            return "Right"
    else:
        return "ND"


while True:
    grabbed, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    coords = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(coords) > 0:
        circle_1 = max(coords, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(circle_1)
        M = cv2.moments(circle_1)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    if type(center) == tuple:
        pts.appendleft(center)
    if len(pts) == 12:
        temp_direction = translation(pts[0], pts[len(pts) - 1])
        if direction != temp_direction:
            direction = temp_direction
    else:
        direction = "ND"
    print(direction)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("E"):
        break
cap.release()
cv2.destroyAllWindows()
