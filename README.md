## D-Map: Occupancy Grid Mapping without Ray-Casting
The paper: [arxiv](https://arxiv.org/abs/2307.08493)  
The original code: [github](https://github.com/hku-mars/D-Map)

---
### Abstract
D-Map is an occupancy grid mapping framework for high-resolution LiDAR that bypasses per-ray traversal. Instead of classical ray-casting (≈ O(B·R) per frame), D-Map (1) infers cell states from a depth image, (2) performs an on-tree update over a tree-based map to avoid revisiting small cells, and (3) **decrementally** removes cells that are confidently KNOWN to shrink the map over time. This repo re-implements the core ideas for a 180° LiDAR in Webots, including a segment-tree RMQ accelerator for depth ranges and an octree map with KNOWN/UNKNOWN/UNDETERMINED states. We provide a ROS 2 wrapper and small benchmarks against a ray-casting baseline.


### Key Innovations
- Depth-image occupancy determination (no per-ray traversal)
- Segment-tree RMQ over the depth image for fast min/max queries
- Octree map + ??? on-tree update (visit only necessary nodes)
- ??? Decremental mapping: remove KNOWN cells to reduce map size

### Performation Results
??

### Quick Start
- Install [Webots](https://cyberbotics.com/doc/guide/installation-procedure)
- Install dependencies
```
pip install -r requirements.txt
```
- Run the Webots world (GUI) and set the robot controller to "Extern"
- In the bot select the controllers as `external`
- From repo root, start the controller:
```
python controllers/main.py --world worlds/dmap.wbt --n 256 --max_range 20
```

### Method Overview
???

### Experiment & Results
- performance scaling
- 

### Citation
```
@article{cai2023dmap,
  title={Occupancy Grid Mapping without Ray-Casting for High-resolution LiDAR Sensors},
  author={Cai, Yixi and Kong, Fanze and Ren, Yunfan and Zhu, Fangcheng and Lin, Jiarong and Zhang, Fu},
  journal={arXiv:2307.08493},
  year={2023}
}
```
