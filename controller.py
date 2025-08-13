import matplotlib.pyplot as plt
from controller import Robot

from src.DMAP import DMap
from src.RAYCASTING import Raycasting
from src.octree import Octree

# * config --------------------
robot = Robot() # type: ignore
time_step = int(robot.getBasicTimeStep())
lidar = robot.getDevice('lidar')
lidar.enable(time_step) # type: ignore


plt.ion()
fig, ax = plt.subplots(1, 1, figsize=(8,6))
# * ---------------------------

# * variables i defined -------------------
n = 20  # grid size
max_dist = 9
cell_size = max_dist / n

robot_x, robot_y = n/2, 0

center = (n/2, n/2)
half = (n/2, n/2)

octree_map = Octree(center, half, max_depth=6)
hash_pixel = set()
# * ---------------------------------------


user_input = input("If you want to process D-MAP (type y)--->\t")

while robot.step(time_step) != -1:
    ranges = lidar.getRangeImage()

    if user_input == 'y' or user_input == 'Y':
        # * DMAP
        visual_grid = DMap(ranges, max_dist, octree_map, n, cell_size, hash_pixel)
    else:
        # * Raycasting
        visual_grid = Raycasting(ranges, max_dist, n, (robot_x, robot_y))


    # * matplotlib code -----------------------------------------
    ax.imshow(visual_grid, cmap='gray', origin='lower', vmin=0, vmax=2)
    ax.plot(robot_x,robot_y, 'ro')
    plt.pause(0.1)
    # * ---------------------------------------------------------