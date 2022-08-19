import csv
from datetime import datetime

def save(lat,lon,K_lat,K_lon,speed,angle,error,deltaT):

    #writing data

    with open('/home/pi/Sensor/data.csv', 'a', newline ='') as f:
        header = ['Latitude','Longtitude','KF_Latitude','KF_Longtitude','Speed','Angle','X_Error','Y_Error','Time']
        writer = csv.DictWriter(f, fieldnames = header)  
        writer.writeheader()
        writer.writerow({       'Latitude':   lat,
                                'Longtitude' : lon,
                                'KF_Latitude':   K_lat,
                                'KF_Longtitude' : K_lon,
                                'Speed': speed,
                                'Angle': angle,
                                'X_Error': error.get("x"),
                                'Y_Error': error.get("y"),
                                'Time': deltaT })

            