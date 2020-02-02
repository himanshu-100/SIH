from constant import eta, NO_OF_DRONE, DRONE_SPEED, BATTERY, set_point, recharge, gamma
import math
import random

def calculate_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def battery_consume(dist):
    return eta * dist


def max_distance_possible(battery):
    return battery / eta


def map_weather_factor(weather):
    if weather == 'clear':
        return 1
    if weather == 'rainy':
        return 2
    if weather == 'wind':
        return 3
    if weather == 'sand':
        return 2.5


def map_elevation_angle(angle):
    if angle == '0':
        return 1
    if (angle == '30'):
        return 1.2
    if (angle == '45'):
        return 1.5
    if angle == '60':
        return 2
    if angle == '90':
        return 10000000


def map_wind_speed(wind_speed, wind_direction=0):
    return wind_speed * (1 / 1 - wind_direction)


def current_speed(top_speed, weather='clear', elevation_angle='0', wind_speed=1, wind_direction=0):
    return top_speed * map_wind_speed(wind_speed, wind_direction) * gamma / (
        map_weather_factor((weather) * map_elevation_angle(elevation_angle)))

def get_position_timewise(index, speed, path):
    positions = []
    speed = 1
    for time in range(0,10):
        curr_time = 0
        flag=0
        for i in range(len(path) - 1):
            dist = calculate_distance(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])
            if (curr_time + dist / speed) < time:
                curr_time = curr_time + dist / speed
            else:
                flag=1
                source_point = path[i]
                dest_point = path[i + 1]
                velocity = speed
                given_time = time - curr_time
                if dest_point[0] == source_point[0]:
                    velocity_cos_value=0
                    velocity_sin_value=1
                else:
                    tan_theta_value = (dest_point[1] - source_point[1]) / (dest_point[0] - source_point[0])
                    theta = math.atan(tan_theta_value)
                    velocity_cos_value = velocity * math.cos(theta)
                    velocity_sin_value = velocity * math.sin(theta)
                x = source_point[0] + velocity_cos_value * given_time
                y = source_point[1] - velocity_sin_value * given_time
                positions.append([x,y])
                break
        if flag==0:
            positions.append(path[len(path)-1])
    return positions

nearest_recharge_coord = []
nearest_recharge_ind = []
points_in_cluster = {}
for i in range(len(recharge)):
    if recharge[i] not in points_in_cluster:
        points_in_cluster[recharge[i]] = []
    points_in_cluster[recharge[i]].append(recharge[i])

for i in range(len(set_point)):
    mini, ind, coord = 100000000, -1, []
    for j in range(len(recharge)):
        if (calculate_distance(set_point[i][0], set_point[i][1], recharge[j][0], recharge[j][1]) < mini):
            mini = calculate_distance(set_point[i][0], set_point[i][1], recharge[j][0], recharge[j][1])
            coord = recharge[j]
            ind = j
    nearest_recharge_coord.append(coord)
    nearest_recharge_ind.append(ind)
    if coord not in points_in_cluster:
        points_in_cluster[coord] = []
    points_in_cluster[coord].append(set_point[i])

source = []
for x, y in points_in_cluster:
    source.append(x)
path = {}
cnt = 0
all_positions = []
for (station_x, station_y), points in points_in_cluster.items():
    random_point = random.choice(points)
    #curr=(station_x,station_y)
    curr = (random_point[0], random_point[1])
    path[(station_x, station_y)] = [curr]
    vis = []
    for j in range(len(points)):
        vis.append(False)
    vis[0] = True
    count = len(points)
    CURR_BATTERY = BATTERY[cnt]
    CURR_SPEED = current_speed(DRONE_SPEED[cnt])
    while count > 0:
        min_dist = 10000000000
        min_ind = -1
        for j in range(len(points)):
            if not vis[j]:
                if min_dist > calculate_distance(curr[0], curr[1], points[j][0], points[j][1]):
                    min_dist = calculate_distance(curr[0], curr[1], points[j][0], points[j][1])
                    min_ind = j
        CURR_BATTERY = CURR_BATTERY - battery_consume(min_dist)
        if (max_distance_possible(CURR_BATTERY) < calculate_distance(points[min_ind][0], points[min_ind][1], station_x,
                                                                     station_y)):
            path[(station_x, station_y)].append((station_x, station_y))
            CURR_BATTERY = BATTERY[cnt] - battery_consume(
                calculate_distance(points[min_ind][0], points[min_ind][1], station_x, station_y))
        vis[min_ind] = True
        curr = points[min_ind]
        path[(station_x, station_y)].append(curr)
        count = count - 1
    cnt = cnt + 1
    print(path[(station_x, station_y)])
    positions = get_position_timewise(cnt, CURR_SPEED, path[(station_x, station_y)])
    print(positions)
    all_positions.append(positions)


import numpy as np
import matplotlib.pyplot as plt

x1 = []
y1 = []
for i in set_point:
    x1.append(i[0])
    y1.append(i[1])
for i in recharge:
    x1.append(i[0])
    y1.append(i[1])

for t in range(0,10):
    x=[]
    y=[]
    plt.figure()
    plt.axis((-10,20,-10,20))
    plt.scatter(x1, y1)

    for i in all_positions:
        x.append(i[t][0])
        y.append(i[t][1])
        plt.scatter(x,y,c='black')

    np.delete(x,0)
    np.delete(y,0)
    name = 'images/pos'+str(t)+'.png'
    plt.savefig(name)
    plt.close()