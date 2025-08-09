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


from occupancy import reset_grid, occupancy_map_generator, pos_gen, occ_state_classifier, update_occtree_occ
from depth_map import depth_map_gen
from cell2depth import c2d_projection, cell_dist
from segmentation import SegTree
from octree import Octree


# * variables i defined -------------------
n = 20
max_dist = 9
cell_size = max_dist / n

robot_x, robot_y = n/2, 0

center = (n/2, n/2)
half = (n/2, n/2)
octree_map = Octree(center, half)

# * ---------------------------------------

while robot.step(time_step) != -1:
    ranges = lidar.getRangeImage()
    depth_map = depth_map_gen(ranges, max_dist)
    seg_tree = SegTree(depth_map.tolist())

    # After creating seg_tree, add these debug prints:
    test_angle = 90  # Look straight ahead
    lidar_dist = seg_tree.query(test_angle, test_angle)
    cell_distance = cell_dist(10, 10, cell_size, n)  # Middle of map

    # print(f"LiDAR dist at angle {test_angle}: {lidar_dist}")
    # print(f"Cell distance for middle: {cell_distance}")
    # print(f"Raw LiDAR ranges sample: {ranges[85:95]}")  # Show some raw data

    # for row in range(n):
    #     for col in range(n):
    #         angle = c2d_projection(row, col, cell_size, n)
    #         cell_distance = cell_dist(row, col, cell_size, n)

    #         state = occ_state_classifier(seg_tree, angle, cell_distance)

    #         if state == 'KNOWN':
    #             occupancy_grid[row, col] = 1
    #         elif state == 'UNKNOWN':
    #             occupancy_grid[row, col] = 0

    update_occtree_occ(octree_map, seg_tree, cell_size, n)
    visual_grid = octree_map.to_grid(n)

    node_count = octree_map.node_count
    print(f"Octree nodes: {node_count}, Grid Cells: {n*n}")
    

    for i, dist in enumerate(ranges):
        if dist < max_dist:
            rad, x, y = pos_gen(i, dist)
            grid_x = floor(x / (max_dist / n)) + floor(n / 2)
            grid_y = floor(y / (max_dist / n))
            if 0 <= grid_x < n and 0 <= grid_y < n:
                visual_grid[grid_y, grid_x] = 2
    
    
    

    # * matplotlib code -----------------------------------------
    ax2.clear()
    ax1.imshow(depth_map.reshape(1, -1), cmap='gray', aspect='auto')
    ax2.imshow(visual_grid, cmap='gray', origin='lower', vmin=0, vmax=2)
    ax2.plot((n)//2,0, 'ro')
    plt.pause(0.1)
    # * ---------------------------------------------------------


