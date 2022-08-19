import L298NHBridge as B
import BNO055
import time

def mag_calibrate():

      B.setMotorRight(-1)
      B.setMotorLeft(1)
      time.sleep(2)
      B.setMotorRight(0)
      B.setMotorLeft(0)
      time.sleep(1)

                  
def turn_targetangle(turn):
      #turn angle has to be from 0 to 180 and -180 to 0 
      stopp_turn = 0
      oldangle = 0
      current_angle = 0

      B.setMotorRight(-0.8)
      B.setMotorLeft(0.8)
      
      while stopp_turn == 0:
            oldangle = current_angle
            north = BNO055.get_mag("north")
            # if north is zero type 
            if north is not None:
                  current_angle = north
            #magnetometer sometime gets interference angle deviation too big     
                  if oldangle - 1 < current_angle < oldangle + 1:
                        newangle = current_angle
                        
                        if newangle - 0.5 < turn < newangle + 0.5:
                              B.setMotorRight(0)
                              B.setMotorLeft(0)
                              stopp_turn = 1
                              print(BNO055.get_mag("north"))

def turn(turn):
      #turn angle has to be from 0 to 180 and -180 to 0 

      currentyaw = BNO055.get_orientation("yaw")
      print(currentyaw)
      if turn > 0: 
            while BNO055.get_orientation("yaw") <  currentyaw + turn:
                  B.setMotorRight(-0.5)
                  B.setMotorLeft(0.5)
                
      else:
            while BNO055.get_orientation("yaw") - 180 >  currentyaw + turn:
                  B.setMotorRight(0.5)
                  B.setMotorLeft(-0.5)
               

      print(BNO055.get_orientation("yaw"))
      B.setMotorRight(0)
      B.setMotorLeft(0)

def stop_car(angle):
    yaw_angle = BNO055.get_orientation('yaw')
    if (yaw_angle is not None):
            yaw = yaw_angle
            print(yaw)
            if  angle - 1 < yaw < angle + 1:
                        B.setMotorRight(0)
                        B.setMotorLeft(0)
                        print('reached')
                        time.sleep(1)
                        return 0
            return 1
                        
                           
                        



