import utm

#take lat,lon
def toUTM(lat,lon):

    info = utm.from_latlon(lat, lon)
    #return x,y
    return info[0],info[1]

#take easting,northing
def toLatLon(x,y):
    
    info = utm.to_latlon(x, y, 33, 'U')
    #return lat,lon
    return  info[0],info[1]


