
def hash_func(col, row) -> str:
    # from occupancy import lidar2grid
    # col, row = lidar2grid(x, y, max_dist, size)
    return f"{col},{row}"

def unhash(hash: str):
    return map(int, hash.split(","))