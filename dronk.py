#引入模組
from __future__ import print_function
from firebase import firebase
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

#連接資料庫(由於設定任何人都能存取，所以不需要設定其他的API Key)
db_url = 'https://dronk-f75d9-default-rtdb.firebaseio.com'
fdb = firebase.FirebaseApplication(db_url, None)
    
#在user下查詢新增的資料(.get讀取)
user = fdb.get('/Order/user', None)  #None全部讀取，1代表讀取第一筆，以此類推
latitude = fdb.get('/Order/latitude', None)
longitude = fdb.get('/Order/longitude', None)

print(user)
print(latitude)
print(longitude)

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

arm_and_takeoff(20)

print("Set default/target airspeed to 5")
vehicle.airspeed = 5

print("Going towards ",user," for 60 seconds...")
target = LocationGlobalRelative(latitude,longitude,20)
vehicle.simple_goto(target)
time.sleep(60)
print("Landing for ",user)
vehicle.mode = VehicleMode("LAND")
# sleep so we can see the change in map
time.sleep(90)

print("Ready to serve ",user)
time.sleep(5)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("Hi ",user)

time.sleep(10)

print("Returning to Base")
arm_and_takeoff(20)
my_location_alt = vehicle.location.global_frame
my_location_alt.lat = 22.9966054
my_location_alt.lon = 120.22163
my_location_alt.alt = 0
vehicle.home_location = my_location_alt
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
