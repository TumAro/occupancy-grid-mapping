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


from occupancy import reset_grid, occupancy_map_generator, pos_gen, occ_state_classifier
from depth_map import depth_map_gen
from cell2depth import c2d_projection, cell_dist
from segmentation import MinSegTree, MaxSegTree


# * variables i defined -------------------
n = 20
max_dist = 9
occupancy_grid = np.zeros((n, n), dtype=int)
cell_size = max_dist / n
# * ---------------------------------------

while robot.step(time_step) != -1:
    ranges = lidar.getRangeImage()
    depth_map = depth_map_gen(ranges, max_dist)
    seg_tree = MinSegTree(depth_map.tolist())

    for row in range(n):
        for col in range(n):
            angle = c2d_projection(row, col, cell_size, n)
            cell_distance = cell_dist(row, col, cell_size, n)

            state = occ_state_classifier(seg_tree, angle, cell_distance)

            if state == 'KNOWN':
                occupancy_grid[row, col] = 1
            elif state == 'UNKNOWN':
                occupancy_grid[row, col] = 0

    for i, dist in enumerate(ranges):
        if dist < max_dist:
            rad, x, y = pos_gen(i, dist)
            grid_x = floor(x / (max_dist / n)) + floor(n / 2)
            grid_y = floor(y / (max_dist / n))
            if 0 <= grid_x < n and 0 <= grid_y < n:
                occupancy_grid[grid_y, grid_x] = 2
    
    
    

    # * matplotlib code -----------------------------------------
    ax2.clear()
    ax1.imshow(depth_map.reshape(1, -1), cmap='gray', aspect='auto')
    ax2.imshow(occupancy_grid, cmap='gray', origin='lower', vmin=0, vmax=2)
    ax2.plot((n)//2,0, 'ro')
    plt.pause(0.1)
    occupancy_grid = reset_grid(n)
    # * ---------------------------------------------------------


