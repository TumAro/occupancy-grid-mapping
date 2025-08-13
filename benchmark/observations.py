# * average time of 10 timesteps iterated for 50 timesteps
dmap = {
    '20': [0.7294416427612305, 0.6023883819580078, 0.5514621734619141, 0.5277693271636963, 0.5135822296142578, 0.504767894744873, 0.49912588936941965, 0.49456655979156494, 0.4906972249348958, 0.48766374588012695],
    '100': [0.8574485778808594, 0.7247805595397949, 0.6649971008300781, 0.6321966648101807, 0.611419677734375, 0.6058653195699056, 0.5954980850219727, 0.5889862775802612, 0.5853123135036893, 0.581059455871582],
    '1000': [1.657724380493164, 1.4924049377441406, 1.424574851989746, 1.3604342937469482, 1.3272380828857422, 1.317318280537923, 1.3074261801583427, 1.302415132522583, 1.3096385531955295, 1.3077354431152344]
}


raycasting = {
    '20': [0.18150806427001953, 0.17426013946533203, 0.17122427622477213, 0.17000436782836914, 0.1688241958618164, 0.1681367556254069, 0.1678807394845145, 0.16767680644989014, 0.1672506332397461, 0.1667499542236328],
    '100':  [0.5996227264404297, 0.5983591079711914, 0.5986452102661133, 0.598365068435669, 0.5991601943969727, 0.6003499031066895, 0.6003447941371373, 0.6000787019729614, 0.6002664566040039, 0.5999326705932617],
    '1000': [5.884194374084473, 5.829215049743652, 5.811516443888347, 5.7945191860198975, 5.783700942993164, 5.780378977457683, 5.816905839102609, 5.837124586105347, 5.862731403774685, 5.892329216003418]   
}

# -------------------------
# -------------------------

import matplotlib.pyplot as plt
import numpy as np

grid_sizes = ['20', '100', '1000']

dmap_times = [dmap[size][-1] for size in grid_sizes]
raycast_times = [raycasting[size][-1] for size in grid_sizes]

# Create comparison chart
# x = np.arange(len(grid_sizes))
# width = 0.35

# fig, ax = plt.subplots(figsize=(10, 6))
# bars1 = ax.bar(x - width/2, dmap_times, width, label='D-Map', color='blue')
# bars2 = ax.bar(x + width/2, raycast_times, width, label='Raycasting', color='red')

# ax.set_xlabel('Grid Size (n×n)')
# ax.set_ylabel('Time (ms)')
# ax.set_title('D-Map vs Raycasting Performance')
# ax.set_xticks(x)
# ax.set_xticklabels([f'{s}×{s}' for s in grid_sizes])
# ax.legend()
# ax.set_yscale('log')  # Log scale to see differences better

# plt.show()

# Show how times stabilize over iterations
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, size in enumerate(grid_sizes):
    axes[i].plot(dmap[size], label='D-Map', marker='o')
    axes[i].plot(raycasting[size], label='Raycasting', marker='s')
    axes[i].set_title(f'Grid {size}×{size}')
    axes[i].set_xlabel('Iteration')
    axes[i].set_ylabel('Time (ms)')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.show()