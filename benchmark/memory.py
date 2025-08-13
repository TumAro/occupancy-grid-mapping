import sys
import numpy as np

def measure_dmap_memory(octree_map):
    """Measure D-Map memory usage (octree nodes)"""
    node_count = octree_map.node_count
    bytes_per_node = 8 * 4
    return node_count * bytes_per_node

def measure_raycasting_memory(n):
    """Measure raycasting memory usage (full grid)"""
    bytes_per_cell = 8  # float64
    return n * n * bytes_per_cell

def memory_comparison(octree_map, n):
    dmap_mem = measure_dmap_memory(octree_map)
    raycast_mem = measure_raycasting_memory(n)

    print(f"Memory Usage (Grid {n}×{n}):")
    print(f"  D-Map: {dmap_mem:,} bytes ({dmap_mem/1024:.1f} KB)")
    print(f"  Raycasting: {raycast_mem:,} bytes ({raycast_mem/1024:.1f} KB)")
    print(f"  D-Map uses {raycast_mem/dmap_mem:.1f}x less memory")

    return dmap_mem, raycast_mem
