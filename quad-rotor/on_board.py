import sys
from dronekit import connect, VehicleMode
from mission_lib import *
from math import sin,cos,atan2,pi
import socket 
import time
#import serial #add 8 wed

print("Start connection pixhawk....")
connection_string = "/dev/ttyACM0"
baud_rate = 115200
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
vehicle.wait_ready('autopilot_version')

print("Finish connect to pixhawk")
#ser = serial.Serial("/dev/ttyACM1",115200) #add 8 wed

#addr = "192.168.1.127"
addr = "192.168.1.160"

dead_zone = 0.05

try:

    s = socket.socket()   

    port = 3000               

    s.connect((addr, port)) 

    while True:
	#status = int(str(ser.readline()).split("\\")[0].split("'")[1]) #add 8 wed
	#if not status <= 1600: #add 8 wed
		#continue #add 8 wed
        data = str(s.recv(1024)).split(']')[0]
        print(data)
        if data == "b''":
            continue
        data = data[3:len(data)-1].split(',')
        
        print("data : ",data)
        
        try:
            xRes , yRes = data
        except Exception:
            print("data error!!")
            time.sleep(1)
            continue

        lat , lon , alt = get_GPSvalue(vehicle)


        if alt < 5:
            continue

        xRes = -1*float(xRes)
        yRes = -1*float(yRes)

        yaw = 0

        yaw = Get_YAW(vehicle)

        want_go = 0.000005

        #if xRes == 100 and yRes == 100: #Can't find
        #    if vehicle.mode == "GUIDED":
        #        vehicle.mode = VehicleMode("AUTO")
        #    else:
        #        continue

        if abs(xRes) < dead_zone and abs(yRes) < dead_zone: #Already found!!

            if vehicle.mode == VehicleMode("AUTO") or vehicle.mode == VehicleMode("GUIDED"):
                print(">>> Change mode to 'QLOITER' <<<<")
                vehicle.mode = VehicleMode("QLOITER")

                Change_Alt(vehicle,15)
                Change_Alt(vehicle,35)
                vehicle.mode = VehicleMode("RTL")

                print("!!!!!!!!!!!!!!!!!! Complete Mission !!!!!!!!!!!!!!!!!!")
                exit()
        

        # print("atan2(yRes,xRes) : ", (atan2(yRes,xRes)*180/pi))

        # if atann < 0:
        #     atann += 2*pi

        if yaw > 0 and yaw <= pi/2:
            n_go = yRes*cos(yaw) - xRes*sin(yaw)
            e_go = yRes*sin(yaw) + xRes*cos(yaw)

        elif yaw > pi/2 and yaw <= pi:
            n_go = xRes*sin(2*pi-yaw) + yRes*cos(2*pi - yaw)
            e_go = xRes*cos(2*pi-yaw) - yRes*sin(2*pi - yaw)

        elif yaw > pi and yaw <= 3*pi/2:
            n_go = xRes*sin(yaw - pi) - yRes*cos(yaw - pi)
            e_go = -xRes*cos(yaw - pi) - yRes*sin(yaw - pi)

        elif yaw > 3*pi/2 and yaw <= 2*pi:
            n_go = -xRes*cos(yaw - pi/2) - yRes*sin(yaw - pi/2)
            e_go = yRes*cos(yaw - pi/2) - xRes*sin(yaw - pi/2)

        elif yaw == 0:
            n_go = yRes
            e_go = xRes

        if abs(n_go) < 0.0000001:
            n_go = 0

        if abs(e_go) < 0.0000001:
            e_go = 0

        n_go = want_go * n_go
        e_go = want_go * n_go

        poslat , poslon , Alt = get_GPSvalue(vehicle)

        if n_go == 0:
            print("e_go : ",e_go+poslon)

        if e_go == 0:
            print("n_go : ",n_go+poslat)


        #if abs(xRes) > 0.12 and abs(yRes) > 0.12 :
        if abs(xRes) >= dead_zone and abs(yRes) >= dead_zone:
            if vehicle.mode == VehicleMode("AUTO") or vehicle.mode == VehicleMode("QLOITER"):
                poslat,poslon,Alt = get_GPSvalue(vehicle) 
                goto(vehicle, poslat+n_go,poslon+e_go,15)


except KeyboardInterrupt:
    s.close()
    print("ERROR : ",e)
    print("Good Bye!!!!!")  
    
