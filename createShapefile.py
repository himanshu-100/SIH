import shapefile
import random

w = shapefile.Writer('shapefiles/map')
w.field('name', 'C')

all = []
for i in range(1,100):
    x = int(random.random()*100)
    y = int(random.random()*100)
    all.append([x, y])
w.multipoint(all)
w.record('location')

recharge = []
for i in range(1,10):
    x = int(random.random()*100)
    y = int(random.random()*100)
    recharge.append([x, y])
w.multipoint(recharge)
w.record('recharge station')

w.close()