import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib

HOST='127.0.0.1'
PORT=3000
lower = np.array([0,189,77])
upper = np.array([6,255,255])
frame_width = 1280
frame_height = 720

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('mask', mask)
    # contours = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(2,2))[1]

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            
            #publish
            publish_center = (int(x), int(y)*-1)
            # c.send(str(publish_center).encode())
            # time.sleep(0.2)

            print('center = {0}'.format(center))
            cv2.circle(frame, center, 2, (0,255,0), 2) #draw center
            print(area)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box],0,(255,0,0),3)


    cv2.waitKey(1)