import socket	
import time
import cv2
import numpy as np

lower = np.array([0,189,77])
upper = np.array([6,255,255])


frame_width = 1280
frame_height = 720

s = socket.socket()	
s1 = socket.socket()

port = 3000				

s.bind(('192.168.1.232', port))		 
print("socket binded to %s" %(port))

s.listen(5)	 
print("socket is listening")
c, addr = s.accept()

cap = cv2.VideoCapture("http://192.168.1.78:8081")

s1.connect(("192.168.1.78",4000))

KeyboardInterrupt

try:

	while True:
		ret, frame = cap.read()
		if not ret:
			print("Can't find image")
			time.sleep(0.5)
			continue

		data = s1.recv(1024)
		print("data : ",data)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower, upper)
		cv2.imshow('mask', mask)
		contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			area = cv2.contourArea(cnt)
			if area > 5000:
				(x,y),radius = cv2.minEnclosingCircle(cnt)
				center = [int(x), int(y)]
				
				#publish
				publish_center = [int(x), int(y)*-1]
				c.send(str(publish_center).encode())
				time.sleep(0.2)

				print('center = {0}'.format(center))
				cv2.circle(frame, center, 2, (0,255,0), 2) #draw center
				print(area)
				rect = cv2.minAreaRect(cnt)
				box = cv2.boxPoints(rect)
				box = np.int0(box)
				cv2.drawContours(frame, [box],0,(255,0,0),3)
		cv2.imshow('result', frame)
		if cv2.waitKey(1) == ord('q'):
			break

except Exception as e:

	print('Error : ',e)
	cap.release()
	cv2.destroyAllWindows()
