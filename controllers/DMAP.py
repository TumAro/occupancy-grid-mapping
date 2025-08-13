from .occupancy import update_occtree_occ
from .depth_map import depth_map_gen
from .segmentation import SegTree
from .occupancy import world2grid, lidar2world
from .hashing import hash_func, unhash

def DMap(ranges, max_dist, octree_map, n, cell_size, hash_pixel):
    depth_map   = depth_map_gen(ranges, max_dist)
    seg_tree    = SegTree(depth_map.tolist())
    update_occtree_occ(octree_map, seg_tree, cell_size, n)
    visual_grid = octree_map.to_grid(n)

    for i, dist in enumerate(ranges):
        if dist < max_dist:
            rad, x, y = lidar2world(i, dist)
            col, row = world2grid(x, y, max_dist, n)
            hash = hash_func(col, row)
            if 0<= col < n and 0 <= row < n:
                if hash not in hash_pixel:
                    hash_pixel.add(hash)

    for hash in hash_pixel:
        col, row = unhash(hash)
        visual_grid[row, col] = 2

    return visual_grid