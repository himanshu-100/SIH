import shapefile
import random

w = shapefile.Writer('shapefiles/map')
w.field('name', 'C')

all = []
for i in range(1,20):
    x = int(random.random()*10)
    y = int(random.random()*10)
    all.append([x, y])
w.multipoint(all)
w.record('location')

recharge = []
for i in range(1,5):
    x = int(random.random()*10)
    y = int(random.random()*10)
    recharge.append([x, y])
w.multipoint(recharge)
w.record('recharge station')

w.close()