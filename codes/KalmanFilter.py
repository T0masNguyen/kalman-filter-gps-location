import numpy as np
from numpy.core.numeric import identity
from numpy.lib.function_base import append
from numpy.linalg import inv
import coordinateconverter as converter
import time

#Initial error covariance matrix  
variance = 3000
P = pow(variance,2)*np.identity(4)

#Errors during estimation
q = 10
Q = q*np.array([[ 1, 0, 0, 0],
              [ 0, 1, 0 ,0],
              [ 0, 0, 1, 0],
              [ 0, 0, 0, 1]])


def filter(X,z,error,deltaT):
    global P
    angle = z[3][0]

    #State matrix
    F = np.array([[1, 0, 0, deltaT*np.cos(angle) ],
                  [0, 1, 0, deltaT*np.sin(angle) ],
                  [0, 0, 1, 0               ],
                  [0, 0 ,0 ,1               ]])

    #Errors during measurement from the gps lib              
    R = np.array([[pow(error.get("x"),2), 0 , 0, 0 ],
                  [0, pow(error.get("y"),2), 0, 0  ],
                  [0, 0,        pow(5,2), 0       ],
                  [0, 0, 0, 0                      ]])        
    #Prediction
    X = F.dot(X) 
    P = F.dot(P).dot(F.T)  + Q
    pre_x,pre_y  =  X[0][0],X[1][0]

    # Calculating the Kalman Gain
    H = np.identity(4)
    S = (H.T).dot(P).dot(H.T) + R
    K = P.dot(H.T).dot(inv(S))

    # Measurement's vector.
    Y = (H.dot(z))

    # Combination of the predicted state, measured values, covariance matrix and Kalman Gain
    X = X + K.dot(Y - H.dot(X))

    # Update Process Covariance Matrix
    P = (np.identity(len(K)) - K.dot(H)).dot(P)

    #Converting the UTM back to longitude and lattitude
    lat,lon = converter.toLatLon(X[0][0],X[1][0])

    #Prediction lat,lon
    pre_lat,pre_lon = converter.toLatLon(pre_x,pre_y)
    
    return lat,lon,pre_lat,pre_lon,X

