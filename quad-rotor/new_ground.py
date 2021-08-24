import sys
import cv2
import time
import numpy as np 
import math
import socket	

try:

    Alt = 2
    
    s = socket.socket()		 
    port = 3000				

    #s.bind(('192.168.1.127', port))
    #s.bind(('192.168.2.104', port))	
    s.bind(('192.168.1.160', port))			 
    print("socket binded to %s" %(port))

    s.listen(5)	 
    print("socket is listening")
    c_socket, addr = s.accept()

    print("socket accept")

    cap = cv2.VideoCapture("rtsp://192.168.2.220:554/stream/1")

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    # cap = cv2.VideoCapture(0)


    # upper = np.array([179, 255, 255])
    # lower = np.array([140, 110, 0])
    upper = np.array([179, 255, 255])
    lower = np.array([155, 0, 0])
    #area_max = 0.0015
    #area_min = 0.0006
    color_send = 1.
    area_res = -1
    area = 0
    wh = (-1, -1)
    w, h = wh

    while True:

        ret,img = cap.read()

        if not ret:
            print("Can't find cam")
            cap = cv2.VideoCapture("rtsp://192.168.2.220:554/stream/1")
            continue

        cv2.imshow('frame',img)

        

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

        r, c, ch = img.shape
        blurred = cv2.GaussianBlur(img, (7, 7), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.dilate(mask, kernel)
        # ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)
        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            xRes = 100.0
            yRes = 100.0
            rect = cv2.minAreaRect(cnt)
            center, wh, _ = cv2.minAreaRect(cnt)
            x, y = center
            w, h = wh
            #w+=1
            #h+=1
            area = cv2.contourArea(cnt)
            area_res = area/(r*c)
            ratio = area/(w*h)

            # Area Conditions
            #if ratio > 0.75 and area_res > 0.0006 : #old
            if ratio > 0.75 and area_res > 0.0006 :
            # if area_res < 0.1056*math.pow(float(Alt)+1,(-1.41))*1.15 and area_res > 0.1056*math.pow(float(Alt)-1,(-1.41))*0.85:
                if (w/h) > 0.85 and (w/h) < 1.17 :
                    xRes = 2*(x - int(c/2))/c
                    yRes = -2*(y - int(r/2))/r
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    blurred = cv2.drawContours(blurred, [box],0,(0,0,255),2)
                    publish_center = [xRes,yRes]
                    c_socket.send(str(publish_center).encode())
                    time.sleep(0.5)
                    print('x:',xRes)
                    print('y:',yRes)
                    print('area:',area_res)
                    print('==========================')

        cv2.waitKey(1)

except KeyboardInterrupt as e:
    s.close()
    time.sleep(2)
    print("Error : ",e)
    
    
