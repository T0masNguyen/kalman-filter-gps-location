import pandas as pd
import gps_calculation as gps


df = pd.read_csv("/home/pi/Sensor/gpsdata.csv")
df.head()

#This was my desired position
targetLat =51.038225
targetLon =13.743346

for i in range(len(df.Latitude)):

    distanceKF,turn_angle = gps.calc(df.KF_Latitude[i],df.KF_Longtitude[i],targetLat,targetLon)
    distanceGPS,turn_angle = gps.calc(df.Latitude[i],df.Longtitude[i],targetLat,targetLon)

    #Measured in meter
    print("KF: : ",distanceKF,"GPS: ",distanceGPS)