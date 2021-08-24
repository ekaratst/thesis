from dronekit import connect, VehicleMode, LocationGlobalRelative, mavutil
from serial import *
import time

def Get_YAW(vehicle):
	yaw = float((str(vehicle.attitude).split(':')[1].split(',')[1])[4:])
	return yaw

def Armed(vehicle):
	print('........Check Armed........')
	while True:
		print(">>>> Change Mode to 'GUIDED' <<<<")
		vehicle.mode = VehicleMode("GUIDED")		
    		print(">>>> ARMED <<<<")
    		vehicle.armed = True
    		if vehicle.armed:
    			print(">>>> Already Armed <<<<")
      			break
    		else:
			continue
    	time.sleep(2)

def Takeoff(vehicle,alt):
	vehicle.mode = VehicleMode("GUIDED")
	print('>>>>>>>> Change mode to GUIED <<<<<<<<<')
 	print('>>>>>>>> Take off <<<<<<<<<')
	vehicle.simple_takeoff(alt)
	time.sleep(3)
	print(">>>> Change mode to 'LOITER' <<<<")
	vehicle.mode = VehicleMode("LOITER")
	print('>>>> Complete Takeoff <<<<')

def Change_Alt(vehicle,want_alt):

	lat, lon, Alt = get_GPSvalue(vehicle)
	
  	print(">>>> Change mode to 'GUIDED' for change alt<<<<")
  	vehicle.mode = VehicleMode("GUIDED")
  	print(">>>> Going to ALT: "+str(want_alt)+" <<<<")

	if Alt < want_alt: # go to higher alt
		while Alt < want_alt:
			lat, lon, Alt = get_GPSvalue(vehicle)
			a_location = LocationGlobalRelative(lat,lon,want_alt)
			vehicle.simple_goto(a_location)
			print("want alt : ",want_alt,", now alt : ",Alt)
			time.sleep(2)
	else: # go to lower alt
		while Alt >= want_alt:
			lat, lon, Alt = get_GPSvalue(vehicle)
			a_location = LocationGlobalRelative(lat,lon,want_alt)
			vehicle.simple_goto(a_location)
			print("want alt : ",want_alt,", now alt : ",Alt)
			time.sleep(2)

  	print(">>>> Change mode to 'QLOITER' for change alt <<<<")
  	vehicle.mode = VehicleMode("QLOITER")
  	print(">>>> Complete Change ALT <<<<")


def goto(vehicle,lat,lon,alt):
 	print(">>>> Change mode to 'GUIDED' <<<<")
  	vehicle.mode = VehicleMode("GUIDED")
  	a_location = LocationGlobalRelative(lat,lon,alt)
  	print('>>>>>>> Going to  '+str(lat)+','+str(lon)+','+str(alt)+' <<<<<<<<<<')
  	vehicle.simple_goto(a_location)
  	time.sleep(3)
  	print(">>> Change mode to 'QLOITER' <<<<")
  	vehicle.mode = VehicleMode("QLOITER")
  	print('>>>> Complete GOTO <<<<')

def land(vehicle):
  	print(">>>> LANDING <<<<")
  	vehicle.mode = VehicleMode("LAND")
  	print(">>>> Landing Complete <<<<")

def get_GPSvalue(vehicle):
	posdata = str(vehicle.location.global_relative_frame).split(':')
  	poslat, poslon, Alt = posdata[1].split(',')
  	lat = float(str(poslat)[4:])
  	lon = float(str(poslon)[4:])
    	alt = float(str(Alt)[4:])
  	return [lat,lon,alt]

def drop(vehicle , servo_num, rpm):
	msg = vehicle.message_factory.command_long_encode(
	0, 0,    # target_system, target_component
	mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
	0, #confirmation
	servo_num,    # servo number
	rpm,          # servo position between 1000 and 2000
	0, 0, 0, 0, 0)    # param 3 ~ 7 not used
	# send command to vehicle
	vehicle.send_mavlink(msg)
	print('Success')
