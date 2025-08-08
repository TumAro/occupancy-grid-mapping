def contains_point(center, half, point) -> bool:
    
    for i, p in enumerate(point):
        if not (center[i] - half[i] <= p <= center[i] + half[i]):
            return False
    return True

def aabb_intersects(center1, half1, center2, half2) -> bool:
    for i in range(len(center1)):
        if not abs(center1[i] - center2[i]) <= (half1[i] + half2[i]):
            return False
    return True

from typing import List, Tuple, Any, Optional
from dataclasses import dataclass, field

Point = Tuple[float, float]

class Node:
    def __init__(self, center: Point, half: Point):
        self.center = center
        self.half = half
        self.points = []
        self.children = None

    @property
    def is_leaf(self):
        return self.children is None
    

    
class Tree:
    def __init__(self, center: Point, half: Point, capacity: int = 4, max_depth: int = 8):
        self.root = Node(center, half)
        self.capacity = capacity
        self.max_depth = max_depth

    def insert(self, point: Point, payload = None) -> bool:

        return self._insert(self.root, point, payload, depth = 0)
    
    def _insert(self, node: Node, point: Point, payload: Any, depth: int):

        if not contains_point(node.center, node.half, point):
            return False

        if (node.is_leaf and 
            (len(node.points) < self.capacity or depth == self.max_depth)):
            node.points.append((point, payload))
            return True
        
        else:
            return True


