from controller import Robot
from math import pi, cos, sin, floor

robot = Robot()
time_step = int(robot.getBasicTimeStep())


lidar = robot.getDevice('lidar')
lidar.enable(time_step)

n = 10

grid = [ [0,]*(n+1) for i in range(n) ]

def print_grid(grid=grid):
    for i in range(n):
        print('\t', grid[i], '\n')

def reset():
    return [ [0,]*n for i in range(n) ]


max_dist = 5.0
cell_size = max_dist / n

while robot.step(time_step) != -1:
    ranges = lidar.getRangeImage()
    
    for i, dist in enumerate(ranges):
        if dist < max_dist:
            angle = (90-i) * pi / 180
            x = dist * cos(angle)
            y = dist * sin(angle)

            grid_x = floor(x / cell_size) + floor(n / 2)
            grid_y = floor(y / cell_size) 

            grid[grid_y][grid_x] = 'X'
    print_grid(grid)
    print('-------------------------------------------------')
    grid = reset()

            # print(f"for angle: {i} | The position ({x:.2f}, {y:.2f})")
    


