import matplotlib.pyplot as plt
import numpy as np

from controller import Robot
from math import pi, cos, sin, floor

# * config --------------------
robot = Robot()
time_step = int(robot.getBasicTimeStep())
lidar = robot.getDevice('lidar')
lidar.enable(time_step)


plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
# * ---------------------------


from occupancy import reset_grid, occupancy_map_generator, pos_gen
from depth_map import depth_map_gen


# * variables i defined -------------------
n = 20
max_dist = 9
occupancy_grid = np.zeros((n, n), dtype=int)
# * ---------------------------------------

while robot.step(time_step) != -1:
    ranges = lidar.getRangeImage()

    for i, dist in enumerate(ranges):
        if dist < max_dist:
            rad, x, y = pos_gen(i, dist)
            occupancy_grid = occupancy_map_generator(occupancy_grid, x, y, max_dist, n)
    
    
    depth_map = depth_map_gen(ranges, max_dist)

    # * matplotlib code -----------------------------------------
    ax2.clear()
    ax1.imshow(depth_map.reshape(1, -1), cmap='gray', aspect='auto', extent=[0, len(ranges), 0, max_dist])
    ax1.set_ylim(0, max_dist)
    ax2.imshow(occupancy_grid, cmap='gray', origin='lower')
    ax2.plot((n+1)//2,0, 'ro')
    plt.pause(0.1)
    occupancy_grid = reset_grid(n)
    # * ---------------------------------------------------------


