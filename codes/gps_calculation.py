from math import *

def calc(lat1, lon1, lat2, lon2):

   lat1 = lat1 # Start lat
   lon1 = lon1 # Start lon
   lat2 = lat2 # Target lat
   lon2 = lon2 # Target lon

   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
   hav_lat = lat2 - lat1
   hav_lon = lon2 - lon1

   ra = sin(hav_lat/2)**2 + cos(lat1) * cos(lat2) * sin(hav_lon/2)**2

   v_angle = asin(sqrt(ra)) 
   h_distance = 2 * 6361 * v_angle * 1000
   #angle to the true north
   target_angle = atan2(sin(hav_lon) * cos(lat2), cos(lat1) \
   * sin(lat2) - sin(lat1) * cos(lat2) * cos(hav_lon))
   #angle is in rad and needs to conert to deg
   target_angle = degrees(target_angle)
   #angle of car to the true north
   if target_angle < 0:
      target_angle = target_angle + 360
      
   return h_distance, target_angle
