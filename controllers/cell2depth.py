from math import pi, atan2, floor

def c2d_projection(row, col, cell_size, size) -> float:
    # we shifting only by x-axis cause we put the bot at (size/2, 0)
    x = (col - size / 2) * cell_size
    y = row * cell_size

    rad = atan2(y, x)
    angle = 180 * (1 - rad / pi)

    return max(0, min(179, floor(angle)))

def cell_dist(row, col, cell_size, n):
    x = (col - n/2) * (cell_size)
    y = row * cell_size
    return (x**2 + y**2)**0.5
