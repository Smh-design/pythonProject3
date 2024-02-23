import akshare as ak
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from random import shuffle
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Fetch stock board industry data
stock_board_industry_name_em_df = ak.stock_board_industry_name_em()

# Extract relevant columns
industry_names = stock_board_industry_name_em_df['板块名称']
percentage_changes = stock_board_industry_name_em_df['涨跌幅']

# Define colors based on the direction of change
colors = ['red' if change > 0 else 'green' for change in percentage_changes]

# Set a scaling factor for the size of the points
scaling_factor = 500

# Create a graph and add nodes
G = nx.Graph()
for industry in industry_names:
    G.add_node(industry)

# Shuffle the nodes to ensure random initial positions
shuffled_nodes = list(G.nodes)
shuffle(shuffled_nodes)

# Add edges based on the distance between nodes
for i in range(len(shuffled_nodes)):
    for j in range(i + 2, len(shuffled_nodes)):
        G.add_edge(shuffled_nodes[i], shuffled_nodes[j])

# Set positions for the labels
label_positions = {industry: (np.random.rand(), np.random.rand()) for industry in industry_names}

# Set a custom figure size
fig, ax = plt.subplots(figsize=(8, 6))

# Draw the graph with spring layout, fixed label positions
pos = nx.spring_layout(G, pos=label_positions, fixed=label_positions.keys())

# Create a scatter plot
scatter = ax.scatter(*zip(*pos.values()), c=colors, s=np.abs(percentage_changes) * scaling_factor)

# Annotate points with industry names and percentage changes
for industry, (x, y) in pos.items():
    change = stock_board_industry_name_em_df.loc[stock_board_industry_name_em_df['板块名称'] == industry, '涨跌幅'].values[0]
    ax.text(x, y, f'{industry}\n{change:.2f}%', ha='center', va='center', fontsize=8)

# Remove x and y axes
ax.axis('off')

# Show the plot
plt.tight_layout()
plt.show()
