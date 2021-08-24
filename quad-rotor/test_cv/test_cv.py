import cv2
import numpy as np

cap = cv2.VideoCapture("http://192.168.43.168:8081/")
# lower = np.array([0,189,77])
# upper = np.array([6,255,255])

while True:
    ret , frame = cap.read()
    while ret:
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, lower, upper)
    # cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)

        cv2.waitKey(1)