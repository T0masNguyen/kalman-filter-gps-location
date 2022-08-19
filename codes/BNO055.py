import adafruit_bno055
import board
import math
import L298NHBridge as B
import time

#Initilizing 
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

#Return car angle to north
def get_mag():
    loop_stop = 1

    while loop_stop:
            if sensor.magnetic != None:
                data_tuple = sensor.magnetic

                calibratedangle = math.atan2(data_tuple[0],data_tuple[1])*(180/math.pi)
 
                # direction of car from 0 to 180
                loop_stop = 0

                if calibratedangle > 0:
                    return 180 - calibratedangle
                    
                # from -179 to 0
                elif calibratedangle <= 0:

                    return 360 + (-180 -(calibratedangle))
                
#Return car rotation angle
def yaw():
    loop_stoop = 1
    while loop_stoop:
        yaw = sensor.euler[0]
        if yaw != None:
            loop_stoop = 0
            return yaw

#Spin the car to the desired angle
def spin(angle):
    mag_target = angle

    #Restore the previous calibration
    restore_calibration()

    mag_car_angle = get_mag()
    time.sleep(2)


    print("Angle to the north of car: ",mag_car_angle)
    time.sleep(2)

    turn = abs(mag_target - mag_car_angle)

    time.sleep(0.5)

    #Power to the wheel
    dc = 1
 
    if turn > 180:
        if mag_target > mag_car_angle:
            B.setMotorRight(dc)
            B.setMotorLeft(-dc)

            
            turn = 360 - turn
            print("Turn left by {} degree!".format(turn))
            stop_car(turn)
            time.sleep(1)

        elif mag_target < mag_car_angle:
            B.setMotorRight(-dc)
            B.setMotorLeft(dc)

            
            turn = 360 - turn
            print("Turn right by {} degree!".format(turn))
            stop_car(turn)
            time.sleep(1)

    elif  turn <= 180: 

        if mag_target > mag_car_angle:
            B.setMotorRight(-dc)
            B.setMotorLeft(dc)
            print("Turn right by {} degree!".format(turn))
            stop_car(turn)
            time.sleep(1)

        elif mag_target < mag_car_angle:
            B.setMotorRight(dc)
            B.setMotorLeft(-dc)
            print("Turn left by {} degree!".format(turn))
            stop_car(turn)
            time.sleep(1)

#Stop the wheel when the car reached the desired angle
def stop_car(angle):
    current_yaw = 0
    start_yaw = yaw()
    print("start_yaw",start_yaw)
    
    while angle > abs(start_yaw-yaw()):
        current_yaw = yaw()
        print("turning angle: ",abs(start_yaw - current_yaw), "magnetic: ",get_mag())

    B.setMotorRight(0)
    B.setMotorLeft(0)
    time.sleep(0.5)
    print('reached')

#Restoring previous calibration
def restore_calibration():
    sensor.mode = adafruit_bno055.CONFIG_MODE
    time.sleep(0.7)
    acceleration = (-35, -16, -31)
    magnetometer = (-491, -725, -310)
    gyro = (-1, -3, 0)
    r_accelerometer = 1000
    r_magnetometer = 668

    #Restore previous data to offsets registers
    sensor.offsets_accelerometer = acceleration
    sensor.offsets_magnetometer = magnetometer
    sensor.offsets_gyroscope = gyro
    sensor.radius_accelerometer = r_accelerometer
    sensor.radius_magnetometer= r_magnetometer

    sensor.mode = adafruit_bno055.NDOF_MODE 
    time.sleep(0.7)
