from typing import List
from math import floor


class MinSegTree:
    def __init__(self, arr: List[float]):
        self.arr = arr
        self.n = len(arr)
        self.tree = [0.0,] * (4*self.n)

        self._build(1, 0, self.n-1)

    def _build(self, node: int, left: int, right: int):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.arr[left]

        mid = int(floor((left +  right) / 2))
        left_val = self._build(2*node, left, mid) or float('inf')
        right_val = self._build(2*node + 1, mid+1, right) or float('inf')
        self.tree[node] = min(left_val, right_val)


    def query(self, start, end, node=1, node_left=0, node_right=None):
        if node_right is None:
            node_right = self.n - 1
        

        if node_left > end or node_right < start:
            return float('inf')

        if node_left >= start and node_right <= end:
            return self.tree[node]

        mid = (node_left + node_right) // 2
        left_min = self.query(start, end, 2*node, node_left, mid)
        right_min = self.query(start, end, 2*node +1, mid+1, node_right)
        return min(left_min, right_min)
    

class MaxSegTree:
    def __init__(self, arr: List[float]):
        self.arr = arr
        self.n = len(arr)
        self.tree = [0.0,] * (4*self.n)

        self._build(1, 0, self.n-1)

    def _build(self, node: int, left: int, right: int):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.arr[left]

        mid = int(floor((left +  right) / 2))
        left_val = self._build(2*node, left, mid) or -float('inf')
        right_val = self._build(2*node + 1, mid+1, right) or -float('inf')
        self.tree[node] = max(left_val, right_val)


    def query(self, start, end, node=1, node_left=0, node_right=None):
        if node_right is None:
            node_right = self.n - 1
        

        if node_left > end or node_right < start:
            return -float('inf')

        if node_left >= start and node_right <= end:
            return self.tree[node]

        mid = (node_left + node_right) // 2
        left_min = self.query(start, end, 2*node, node_left, mid)
        right_min = self.query(start, end, 2*node +1, mid+1, node_right)
        return max(left_min, right_min)



# test_arr = [5.0, 2.0, 8.0, 1.0, 3.0]
# seg_tree = SegTree(test_arr)

# print(seg_tree.query(1, 3))
# print(seg_tree.query(0, 1))