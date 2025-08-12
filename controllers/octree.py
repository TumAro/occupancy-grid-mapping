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
import itertools
import numpy as np

Point = Tuple[float, ...]
Payload = Any

class Node:
    def __init__(self, center: Point, half: Point):
        self.center = center
        self.half = half
        self.children: Optional[List[Node]] = None
        
        self.state = 'UNDETERMINED'

    @property
    def is_leaf(self):
        return self.children is None
    

class Octree:
    def __init__(self, center: Point, half: Point, max_depth: int = 8):
        self.root = Node(center, half)
        self.max_depth = max_depth

    def insert(self, point: Point, payload = None) -> bool:

        return self._insert(self.root, point, payload, depth = 0)
    
    def _insert(self, node: Node, point: Point, payload: Any, depth: int):

        if not contains_point(node.center, node.half, point):
            return False

        if node.is_leaf:
            if node.state == 'UNDETERMINED' and depth < self.max_depth:
                self._subdivide(node)
                return True
            
        if node.children is not None:
            for child in node.children:
                if contains_point(child.center, child.half, point):
                    return self._insert(child, point, payload, depth+1)
            
        return True
    
    @property
    def node_count(self):
        return self._count_nodes(self.root)

    def _count_nodes(self, node: Node):
        if node.is_leaf:
            return 1
        return 1 + sum(self._count_nodes(child) for child in node.children) # type: ignore

    
    def _subdivide(self, node: Node):
        if node.children is not None:
            return
        
        D = len(node.center)
        child_half = tuple(h / 2 for h in node.half)

        children = []
        for signs in itertools.product((-1, 1), repeat=D):
            center = tuple(c + s*h for c, s, h in zip(node.center, signs, child_half))
            children.append(Node(center, child_half))

        node.children = children

    def update_tree(self):
        self.root = self._remove_known(self.root)
    
    def _remove_known(self, node: Node):
        if node is None:
            return None
        
        #! removing all descendants
        if node.state == 'KNOWN':
            return None
        
        if node.children is not None:
            new_children = []
            for child in node.children:
                result = self._remove_known(child)
                if result is not None:          # ! keep not  known children
                    new_children.append(result)

            if len(new_children) == 0:
                node.children = None
            else:
                node.children = new_children

        return node

    def to_grid(self, n: int):
        grid = np.zeros((n, n))

        def fill_node(node: Node):
            if node is None:
                return
            
            # the bounds of this node
            min_row = max(0, int(node.center[1] - node.half[1]))
            max_row = min(n, int(node.center[1] + node.half[1]))
            min_col = max(0, int(node.center[0] - node.half[0]))
            max_col = min(n, int(node.center[0] + node.half[0]))

            if node.state == 'KNOWN':
                grid[min_row:max_row, min_col:max_col] = 1
            elif node.state == 'UNKNOWN':
                grid[min_row:max_row, min_col:max_col] = 0

            if not node.is_leaf:
                for child in node.children: # type: ignore
                    fill_node(child)

        fill_node(self.root)
        return grid


            


