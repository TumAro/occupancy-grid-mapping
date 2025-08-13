import numpy as np

def calc_acc(dmap_grid, ray_grid, n):

    tot_cells = dmap_grid.size
    matching_cells = np.sum(dmap_grid == ray_grid)
    acc = (matching_cells / tot_cells) * 100

    dmap_occupied = np.sum(dmap_grid == 2)
    raycast_occupied = np.sum(ray_grid == 2)

    print(f"""{n} x {n} --->
Accuracy: {acc:.1f}%
D-map Obstacles: {dmap_occupied}, Raycasting Obstacles: {raycast_occupied}
""")
    return acc