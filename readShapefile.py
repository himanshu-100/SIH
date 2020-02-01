import shapefile

sf = shapefile.Reader("shapefiles/map")
s = sf.shape(0)
all = s.points
print(all)

s = sf.shape(1)
recharge = s.points
print(recharge)