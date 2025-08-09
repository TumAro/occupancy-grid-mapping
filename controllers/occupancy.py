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

def occ_state_classifier(tree, start_a, end_a, cell_min_dist, cell_max_dist):
    min_dist, max_dist = tree.query(start_a, end_a)
    if min_dist == 0:           # no LiDAR hits
        return 'UNKNOWN'
    elif max_dist < cell_min_dist:  # Object blocks view to cell
        return 'UNKNOWN'
    elif min_dist > cell_max_dist:  # Cell is free
        return 'UNKNOWN'
    else:
        return 'UNDETERMINED'
    
from octree import Node, Octree
from cell2depth import c2d_projection, cell_dist

def update_occtree_occ(tree: Octree, seg_tree, cell_size, n):

    def process_node(node: Node, depth):
        if depth >= tree.max_depth:
            return
        
        min_row = max(0, int(node.center[1] - node.half[1]))
        max_row = min(n-1, int(node.center[1] + node.half[1]))
        min_col = max(0, int(node.center[0] - node.half[0]))
        max_col = min(n-1, int(node.center[0] + node.half[0]))

        start_angle = c2d_projection(min_row, min_col, cell_size, n)
        end_angle = c2d_projection(max_row, max_col, cell_size, n)

        min_dist = cell_dist(min_row, min_col, cell_size, n)
        max_dist = cell_dist(max_row, max_col, cell_size, n)

        # DEBUG PRINTS
        print(f"Node center: {node.center}, half: {node.half}")
        print(f"Angles: {start_angle} to {end_angle}, Distances: {min_dist:.1f} to {max_dist:.1f}")



        state = occ_state_classifier(seg_tree, min(start_angle, end_angle), max(start_angle, end_angle), min_dist, max_dist)
        print(f"State: {state}")

        node.state = state
        # print(f"Root node state: {node.state}")
        if state == 'UNDETERMINED' and node.is_leaf:
            tree._subdivide(node)
            for child in node.children:
                process_node(child, depth + 1)
    
    process_node(tree.root, 0)

    