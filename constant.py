import shapefile

sf = shapefile.Reader("shapefiles/map")
s = sf.shape(1)
recharge = s.points

s = sf.shape(0)
set_point = s.points

NO_OF_DRONE = 5
DRONE_SPEED = [0.8,0.9,1.1,1.2,1.3]
BATTERY = [100,60,70,150,30]
MAX_X_COORD = 100
MIN_X_COORD = 0
MAX_Y_COORD = 100
MIN_Y_COORD = 0
eta = 1.3
gamma = 0.73
