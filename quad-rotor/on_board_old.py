import sys
from dronekit import connect, VehicleMode
from mission_lib import *
from math import sin,cos,atan2,pi
import socket 
import serial #add 8 wed

print("Start connection pixhawk....")
connection_string = "/dev/ttyACM0" # ls /dev 
baud_rate = 115200
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
vehicle.wait_ready('autopilot_version')

print("Finish connect to pixhawk")

ser = serial.Serial("/dev/ttyACM1",115200) #add 8 wed

addr = "192.168.1.232" #mycomputer edit!

dead_zone = 0.05 # can edit

try:

    s = socket.socket()   

    port = 3000               

    s.connect((addr, port)) 

    c, addr = s.accept()

    while True: 
        status = int(str(ser.readline()).split("\\")[0].split("'")[1]) #add 8 wed
        if not status <= 1700: #add 8 wed
            continue #add 8 wed

        data = str(s.recv(1024))
        #print(data)
        if data == "b''":
            continue
        data = data[3:len(data)-2].split(',')
        
        print("data : ",data)
        
        try:
            xRes , yRes = data
        except Exception:
            print("data error!!")
            continue

        lat , lon , alt = get_GPSvalue(vehicle)

        c.send(str(alt))

        if alt < 5:
            continue

        xRes = float(xRes) # wait to test can edit
        yRes = float(yRes) # wait to test can edit

        yaw = 0

        yaw = Get_YAW(vehicle)

        want_go = 0.0000001 # wait to test can edit

        ######### comment
        # if xRes == 100 and yRes == 100: #Can't find
        #     if vehicle.mode == "GUIDE":
        #         vehicle.mode = VehicleMode("AUTO")
        #     else:
        #         continue
        ######### comment

        if abs(xRes) < dead_zone and abs(yRes) < dead_zone: #Already found and center!! # can edit 0,05
            # check mode in  rpi
            print(">>> Change mode to 'QLOITER' <<<<")
            vehicle.mode = VehicleMode("QLOITER") 

            Change_Alt(vehicle,15) # decend to drop
            #drop(vehicle, servo_num , rpm) # add in rpi
            Change_Alt(vehicle,35) # increse hight for RTL
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


        if abs(xRes) >= dead_zone and abs(yRes) >= dead_zone: #already found!! edit in rpi add =
            if vehicle.mode == "AUTO" or vehicle.mode == "QLOITER": #edit add mode in rpi
                poslat,poslon,Alt = get_GPSvalue(vehicle) 
                mission_lib.goto(vehicle, poslat+n_go,poslon+e_go,Alt)


except Exception as e:
    s.close()
    print("ERROR : ",e)
    print("Good Bye!!!!!")  
    
