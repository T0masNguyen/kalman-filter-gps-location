import time
import L298NHBridge as Bridge
import KalmanFilter as KF
import coordinateconverter as converter
import gpsd
import gps_calculation as gps
from savinggpsdata import save
import BNO055
import numpy as np
import os,readchar
from threading import Thread

#Interface
def getch():
   ch = readchar.readchar()
   return ch

#Initializing start position
lat0 = 0
lon0 = 0
stop = 0

#Desired position
targetLat =51.038225
targetLon =13.743346

#Run thread to find the accurate start position
def start_pos():
    while True:
        global lat0,lon0,stop,X
        packet = gpsd.get_current()
        if packet.lat != 0:
                x,y = converter.toUTM(packet.lat,packet.lon)
                #Initial state
                X = np.array([[x],
                              [y],
                              [BNO055.get_mag("north")],
                              [Bridge.speed()]])

                z = np.array([[x],
                              [y],
                              [BNO055.get_mag("north")],
                              [Bridge.speed()]])
                deltaT = time.time() - t
                t = time.time()
                lat0,lon0,pre_lat,pre_lon,X = KF.filter(X,z,packet.error,deltaT)

        if stop:
            distance,turn_angle = gps.calc(lat0,lon0,targetLat,targetLon)
            print("Start position: ", lat0, lon0, "Distance: ",distance)
            break

if __name__ == "__main__":

    #Activating GPS
    #Direct gps to port with command: sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
    gpsd.connect()

    #Initialzing starting position
    X = np.array([0],
                 [0],
                 [0],
                 [0])

    #Time between each measured data
    t = time.time()

    #Running thread to find starting position
    t1 = Thread(target = start_pos)
    t1.start()

    # 3 seconds for filter to approaximate the start position
    time.sleep(3)
    stop = 1

    while True:

        print("Press s to start program!")
        print("Press x to end program!")
        char = getch()

        if(char == "s"): 
            os.system('clear')
            #Activating GPS
            #Direct gps to port with command: sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
            packet = gpsd.get_current()

            #Angle toward target
            distance,turn_angle = gps.calc(lat0,lon0,targetLat,targetLon)
            print("Target angle: ",turn_angle)
            BNO055.spin(turn_angle)
             
            #Detecting gaps for speed and distance calculation
            Bridge.gapdetection()
            
            while True:
                packet = gpsd.get_current()

                if packet.lon == 0:
                    Bridge.setMotorLeft(0)
                    Bridge.setMotorRight(0)

                if packet.lon != 0:
                    Bridge.setMotorLeft(0.5)
                    Bridge.setMotorRight(0.5) 

                    #Converting lat and lon to utm  
                    x,y = converter.toUTM(packet.lat,packet.lon)

                    #Measurement vector
                    angle = BNO055.get_mag("north")
                    speed = Bridge.speed()
                    z = np.array([[x],
                                  [y],
                                  [angle],
                                  [speed]])

                    #Time difference between measurement
                    deltaT = time.time() - t
                    t = time.time()

                    #Filtering
                    K_lat,K_lon,pre_lat,pre_lon,X = KF.filter(X,z,packet.error,deltaT)

                    #Writing data 
                    save(packet.lat,packet.lon,K_lat,K_lon,speed,angle,packet.error,deltaT)

                    #Updating distance
                    distanceKF,turn_angle = gps.calc(K_lat,K_lon,targetLat,targetLon)
                    distanceGPS,turn_angle = gps.calc(packet.lat,packet.lon,targetLat,targetLon)
                    distanceEstimation,turn_angle = gps.calc(pre_lat,pre_lon,targetLat,targetLon)
                    print("KF : ",distanceKF,"GPS: ",distanceGPS, "Prediction: ",distanceEstimation)

                    if distanceKF < 4:
                        print("Reached the target!")
                        Bridge.setMotorLeft(0)
                        Bridge.setMotorRight(0)
                        Bridge.exit()
                        break
                        
                    if(char == "x"):
                        os.system('clear')
                        Bridge.setMotorLeft(0)
                        Bridge.setMotorRight(0)
                        Bridge.exit()
                        print("Program Ended!")
                        break


        if(char == "x"):
            os.system('clear')
            Bridge.setMotorLeft(0)
            Bridge.setMotorRight(0)
            Bridge.exit()
            print("Program Ended!")
            break
        char = ""
