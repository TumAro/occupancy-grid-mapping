import numpy as np
from math import pi, cos, sin, floor


def reset_grid(size):
    return np.zeros((size, size), dtype=int)

def lidar2world(angle, dist):
    rad = pi * (1 - (angle / 180))
    x = dist * cos(rad)
    y = dist * sin(rad)

    return rad, x, y

def world2grid(x, y, max_dist, size):
    grid_x = floor(x / (max_dist / size)) + floor(size / 2)
    grid_y = floor(y / (max_dist / size))

    return grid_x, grid_y

def occupancy_map_generator(grid, x, y, max_dist, size):
    grid_x, grid_y = world2grid(x, y, max_dist, size)

    if 0 <= grid_x < size and 0 <= grid_y < size:
        grid[grid_y, grid_x] = 1

    return grid

#! DEBUG ONLY
debug_count = {
    'KNOWN': 0,
    'UNKNOWN': 0,
    'UNDETERMINED': 0
}

def occ_state_classifier(tree, start_a, end_a, cell_min_dist, cell_max_dist, threshold=0.8):
    min_dist, max_dist, count = tree.query(start_a, end_a)

    if count == 0:
        return 'KNOWN'    # unobserved


    proj_pixels = max(1, (end_a - start_a +1))
    alpha = count / proj_pixels


    
    if alpha > threshold:
        if max_dist < cell_min_dist:  # Object blocks view to cell
            return 'UNKNOWN'
        elif min_dist > cell_max_dist:  # Cell is free
            return 'KNOWN'
        else:
            return 'UNDETERMINED'
        
    else:
        if min_dist > cell_max_dist:
            return 'KNOWN'
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

        cell_min = cell_dist(min_row, min_col, cell_size, n)
        cell_max = cell_dist(max_row, max_col, cell_size, n)


        state = occ_state_classifier(
                seg_tree,
                min(start_angle, end_angle),
                max(start_angle, end_angle),
                min(cell_min, cell_max),
                max(cell_min, cell_max),
            )
        
        debug_count[state] += 1
        node.state = state
        # print(f"*** MARKING NODE AS KNOWN at depth {depth} ***")
        if state == 'UNDETERMINED' and node.is_leaf:
            tree._subdivide(node)
            for child in node.children: # type: ignore
                process_node(child, depth + 1)

    process_node(tree.root, 0)
    print(debug_count) #!

    