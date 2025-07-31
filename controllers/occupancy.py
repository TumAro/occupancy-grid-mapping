import numpy as np
from math import pi, cos, sin, floor


def reset_grid(size):
    return np.zeros((size, size), dtype=int)

def pos_gen(angle, dist):
    rad = pi * (1 - (angle / 180))
    x = dist * cos(rad)
    y = dist * sin(rad)

    return rad, x, y

def occupancy_map_generator(grid, x, y, max_dist, size):
    grid_x = floor(x / (max_dist / size)) + floor(size / 2)
    grid_y = floor(y / (max_dist / size))

    if 0 <= grid_x < size and 0 <= grid_y < size:
        grid[grid_y, grid_x] = 1

    return grid

