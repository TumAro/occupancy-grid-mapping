import matplotlib.pyplot as plt
from controller import Robot
import numpy as np

from controllers.DMAP import DMap
from controllers.RAYCASTING import Raycasting
from controllers.octree import Octree

from benchmark.benchmark import benchmark_process
from benchmark.memory import memory_comparison



# * config --------------------
robot = Robot()
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


frame_count = 0
total_time = 0
data = []


print("\nAverage time taken when using Raycasting")
print(f"""--------------------------
Grid Size:\t{n} x {n}
max_lidar_dist:\t{max_dist}
Average frames:\t{10}
--------------------------
""")
while robot.step(time_step) != -1:
    frame_count += 1

    ranges = lidar.getRangeImage() # type: ignore
    
    # * DMAP
    # visual_grid, process_time = benchmark_process(DMap, ranges, max_dist, octree_map, n, cell_size, hash_pixel)
    
    # * Raycasting
    visual_grid, process_time = benchmark_process(Raycasting, ranges, max_dist, n, (robot_x, robot_y))


    # ! Time benchmarking
    total_time += process_time
    if frame_count % 10 == 0:
        avg_ms = total_time / frame_count 
        data.append(avg_ms)
        print(f"Average Time: {avg_ms:.2f}ms")
    
    

    # * matplotlib code -----------------------------------------
    ax.imshow(visual_grid, cmap='gray', origin='lower', vmin=0, vmax=2)
    ax.plot(robot_x,robot_y, 'ro')
    plt.pause(0.1)
    # * ---------------------------------------------------------

    if frame_count == 100:
        print('\n', data)
        break