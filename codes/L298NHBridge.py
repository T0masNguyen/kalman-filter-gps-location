import RPi.GPIO as io
import time
import math

io.setmode(io.BCM)
# Power input
DC_MAX = 100
# Delete warning
io.setwarnings(False)
IN1 = 21
IN2 = 20
IN3 = 16
IN4 = 26
ENA = 27
ENB = 22
#Right motor setup
rightmotor_in1_pin = IN1
rightmotor_in2_pin = IN2
io.setup(rightmotor_in1_pin, io.OUT)
io.setup(rightmotor_in2_pin, io.OUT)

#Left motor setup
leftmotor_in1_pin = IN3
leftmotor_in2_pin = IN4
io.setup(leftmotor_in1_pin, io.OUT)
io.setup(leftmotor_in2_pin, io.OUT)
 

#Stop the car at start
io.output(leftmotor_in1_pin, False)
io.output(leftmotor_in2_pin, False)
io.output(rightmotor_in1_pin, False)
io.output(rightmotor_in2_pin, False)

#setup ENA,ENB

rightmotorpwm_pin = ENA
leftmotorpwm_pin = ENB
io.setup(rightmotorpwm_pin, io.OUT)
io.setup(leftmotorpwm_pin, io.OUT)
rightmotorpwm = io.PWM(rightmotorpwm_pin,100)
leftmotorpwm = io.PWM(leftmotorpwm_pin,100)


#0 pwm at start
leftmotorpwm.start(0)
leftmotorpwm.ChangeDutyCycle(0)
rightmotorpwm.start(0)
rightmotorpwm.ChangeDutyCycle(0)

#Light Sensor
#5 left, 6 right
io.setup(6, io.IN)
io.setup(5, io.IN)

#Initializing variables
rpm = 0
rightgap_counter = 0
gap_counter = 0
previous_time = 0
v = 0
rotation_distance = 0
velocity = 0
global distance
distance = 0

def rightwheel(channel):
    global rightgap_counter, rpm, previous_time
    rightgap_counter = rightgap_counter + 1
    if rightgap_counter >= 20:
        timetaken = int(round(time.time() * 1000)) - previous_time
        rpm = (1000/timetaken) * 60
        previous_time = int(round(time.time() * 1000))
        rightgap_counter = 0

def leftwheel(channel):
    global gap_counter
    gap_counter = gap_counter + 1

def gapdetection():
   io.add_event_detect(6,io.RISING,callback=rightwheel)
   io.add_event_detect(5,io.RISING,callback=leftwheel)

def speed():
    global velocity
    # 0.033 = radius of wheel
    # Velocity = 2π × RPS × radius of wheel.
    velocity = 0.033 * rpm * 0.104
    return velocity

def distance():
   # 0.033 = radius of wheel
   distance = (2*math.pi*0.033) * (gap_counter/20)
   return distance

def setMotorMode(motor, mode):
   if motor == "leftmotor":
      if mode == "reverse":
         io.output(leftmotor_in1_pin, False)
         io.output(leftmotor_in2_pin, True)
      elif  mode == "forward":
         io.output(leftmotor_in1_pin, True)
         io.output(leftmotor_in2_pin, False)
      else:
         io.output(leftmotor_in1_pin, False)
         io.output(leftmotor_in2_pin, False)
         
   elif motor == "rightmotor":
      if mode == "reverse":
         io.output(rightmotor_in1_pin, True)
         io.output(rightmotor_in2_pin, False)
      elif  mode == "forward":
         io.output(rightmotor_in1_pin, False)
         io.output(rightmotor_in2_pin, True)
      else:
         io.output(rightmotor_in1_pin, False)
         io.output(rightmotor_in2_pin, False)
   else:
      io.output(leftmotor_in1_pin, False)
      io.output(leftmotor_in2_pin, False)
      io.output(rightmotor_in1_pin, False)
      io.output(rightmotor_in2_pin, False)

def setMotorLeft(power):
   int(power)
   if power < 0:

      setMotorMode("leftmotor", "reverse")
      pwm = -int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   elif power > 0:

      setMotorMode("leftmotor", "forward")
      pwm = int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   else:

      setMotorMode("leftmotor", "stopp")
      pwm = 0
   leftmotorpwm.ChangeDutyCycle(pwm)

def setMotorRight(power):
   int(power)
   if power < 0:
      setMotorMode("rightmotor", "reverse")
      pwm = -int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   elif power > 0:
      setMotorMode("rightmotor", "forward")
      pwm = int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   else:
      setMotorMode("rightmotor", "stopp")
      pwm = 0
   rightmotorpwm.ChangeDutyCycle(pwm)
   
def exit():
   io.output(leftmotor_in1_pin, False)
   io.output(leftmotor_in2_pin, False)
   io.output(rightmotor_in1_pin, False)
   io.output(rightmotor_in2_pin, False)
   io.cleanup()
