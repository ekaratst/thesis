from dronekit import connect, VehicleMode
from mission_lib import *

connection_string = "/dev/ttyACM0"
baud_rate = 115200
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
vehicle.wait_ready('autopilot_version')

drop(vehicle, servo_num , rpm)
