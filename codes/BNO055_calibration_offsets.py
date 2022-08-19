import csv
from datetime import datetime
import BNO055 as B
import time

now = datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

with open('/home/pi/Sensor/offsets_{} .csv'.format(now), 'a', newline ='') as f:
    header = ['A','M','G','RA','RM']
    writer = csv.DictWriter(f, fieldnames = header)
    writer.writeheader()


def save(A,M,G,RA,RM):
    
    #writing data
    with open('/home/pi/Sensor/offsets_{} .csv'.format(now), 'a', newline ='') as f:
        header = ['A','M','G','RA','RM']
        writer = csv.DictWriter(f, fieldnames = header)  
        writer.writerow({        'A':   A,
                                'M' : M,
                                'G':   G,
                                'RA' : RA,
                                'RM': RM })

stop = 1
while stop:
    print(B.sensor.calibration_status,B.sensor.calibrated)
    if B.sensor.calibrated:
        stop = 0 


time.sleep(0.5)
A = B.sensor.offsets_accelerometer
M = B.sensor.offsets_magnetometer
G = B.sensor.offsets_gyroscope
RA = B.sensor.radius_accelerometer
RM = B.sensor.radius_magnetometer
print(A)
print(M)
print(G)
print(RA)
print(RM)

save(A,M,G,RA,RM)

