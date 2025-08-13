import numpy as np
from .occupancy import reset_grid, lidar2world, world2grid

def bresenham_line(x0, y0, x1, y1):
    points = []
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0

    while True:
        points.append((x,y))

        if x == x1 and y == y1:
            break
        
        e2 = 2*err
        if e2 > -dy:
            err -= dy
            x += sx

        if e2 < dx:
            err += dx
            y += sy

    return points


def Raycasting(ranges, max_dist, n, robot_grid_pos):
    grid = reset_grid(n)

    robot_x, robot_y = robot_grid_pos

    for i, dist in enumerate(ranges):
        if dist >= max_dist:
            continue

        # getting the x,y for world and the grid indexes
        rad, x, y = lidar2world(i, dist)
        grid_x, grid_y = world2grid(x, y, max_dist, n)

        # Bresenham Line algorithm
        x0, y0 = int(robot_x), int(robot_y)
        x1, y1 = int(grid_x), int(grid_y)
        ray_points = bresenham_line(x0, y0, x1, y1)

        for i, (x,y) in enumerate(ray_points):
            if 0 <= x < n and 0 <= y < n:
                if i == len(ray_points) - 1:
                    grid[y, x] = 2
                else:
                    grid[y, x] = 1

    return grid
