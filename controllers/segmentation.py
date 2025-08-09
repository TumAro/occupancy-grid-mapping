from typing import List
from math import floor


class SegTree:
    def __init__(self, arr: List[float]):
        self.arr = arr
        self.n = len(arr)
        self.tree = [(0.0,0.0),] * (4*self.n)

        self._build(1, 0, self.n-1)

    def _build(self, node: int, left: int, right: int):
        if left == right:
            val = self.arr[left]
            self.tree[node] = (val, val)
            return (val, val)

        mid = int(floor((left +  right) / 2))
        left_min, left_max = self._build(2*node, left, mid)
        right_min, right_max = self._build(2*node + 1, mid+1, right)


        node_min = min(left_min, right_min)
        node_max = max(left_max, right_max)
        self.tree[node] = (node_min, node_max)
        return (node_min, node_max)


    def query(self, start, end, node=1, node_left=0, node_right=None):
        if node_right is None:
            node_right = self.n - 1
        

        if node_left > end or node_right < start:
            return (float('inf'), -float('inf'))

        if node_left >= start and node_right <= end:
            return self.tree[node]

        mid = (node_left + node_right) // 2
        left_min, left_max = self.query(start, end, 2*node, node_left, mid)
        right_min, right_max = self.query(start, end, 2*node + 1, mid+1, node_right)
        
        return (min(left_min, right_min), max(left_max, right_max))
