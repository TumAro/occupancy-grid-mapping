import numpy as np

def depth_map_gen(ranges, max_dist):
    map = np.zeros(180, dtype=float)
    for i, dist in enumerate(ranges):
        if dist <= max_dist:
            map[i] = dist
    return map


