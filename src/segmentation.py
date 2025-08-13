from typing import List
from math import floor


class SegTree:
    def __init__(self, arr: List[float]):
        self.arr = arr
        self.n = len(arr)
        self.tree = [(float('inf'), -float('inf'), 0)] * (4*self.n)

        self._build(1, 0, self.n-1)

    def _build(self, node: int, left: int, right: int):
        if left == right:
            val = self.arr[left]
            if val > 0:
                self.tree[node] = (val,val,1)
            else:
                self.tree[node] = (float('inf'), -float('inf'), 0)
            return self.tree[node]

        mid = (left +  right) // 2
        a = self._build(2*node, left, mid)
        b = self._build(2*node + 1, mid+1, right)

        self.tree[node] = (min(a[0], b[0]), max(a[1], b[1]), a[2]+b[2])
        return self.tree[node]

    def query(self, start, end, node=1, node_left=0, node_right=None):
        if node_right is None:
            node_right = self.n - 1

        if node_left > end or node_right < start:
            return (float('inf'), -float('inf'), 0)

        if node_left >= start and node_right <= end:
            return self.tree[node]

        mid = (node_left + node_right) // 2
        a = self.query(start, end, 2*node, node_left, mid)
        b = self.query(start, end, 2*node+1, mid+1, node_right)
        
        return (min(a[0], b[0]), max(a[1], b[1]), a[2]+b[2])
