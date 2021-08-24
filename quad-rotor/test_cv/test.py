import cv2

cap = cv2.VideoCapture("rtsp://192.168.2.220:554/stream/1")

while True:
    ret , frame = cap.read()
    if not ret:
        print("can't find")
        continue
    cv2.imshow('frame',frame)
    cv2.waitKey(1)