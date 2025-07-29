import matplotlib.pyplot as plt
import numpy as np

from controller import Robot
from math import pi, cos, sin, floor

def clamp(val, lower, upper):
    return max(lower, min(val, upper))

robot = Robot()
time_step = int(robot.getBasicTimeStep())


lidar = robot.getDevice('lidar')
lidar.enable(time_step)

n = 20

grid = np.zeros((n, n+1), dtype=int)
plt.ion()
fig, ax = plt.subplots()


def reset():
    return np.zeros((n, n+1), dtype=int)


max_dist = 5.0
cell_size = max_dist / n

# test_grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]

def _set_grid(grid, x, y):
    h = grid.shape[0]
    grid[y, x] = 1


while robot.step(time_step) != -1:
    ranges = lidar.getRangeImage()
    
    for i, dist in enumerate(ranges):
        if dist < max_dist:
            angle = pi * (1 - (i / 180))
            x = dist * cos(angle)
            y = dist * sin(angle)

            grid_x = floor(x / (max_dist / (n+1))) + floor(n / 2)
            grid_y = floor(y / cell_size)

            _set_grid(grid, grid_x, grid_y)

    
    ax.clear()
    ax.imshow(grid, cmap='gray', origin='lower')
    ax.plot((n+1)//2, 0, 'ro')
    plt.pause(0.1)
    grid = reset()

            # print(f"for angle: {i} | The position ({x:.2f}, {y:.2f})")

