import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from parser import parse_csv

# Load data from CSV into the graph
graph = parse_csv('edgeinformation.csv')

# Create an undirected graph
G = nx.Graph()

# Add edges from the adjacency list
for node in graph:
    for neighbor, weight in graph[node]:
        # Skip edges with weight 999
        if weight == 999:
            continue
        G.add_edge(node, neighbor, weight=weight)

# Calculate the distances for the layout positions
def custom_distance(u, v, weight):
    if weight == 999:
        return 1e6  # Set a very large distance for inaccessible edges
    return 1.0 / weight  # Inverse of weight to increase distance for higher weights

# Define fixed positions for specific nodes
fixed_positions = {
    1: (0, 1),    # Node 1 fixed at top left
    6: (1, 1),    # Node 6 fixed at top right
    98: (0, 0),   # Node 98 fixed at bottom left
    112: (1, 0)   # Node 112 fixed at bottom right
}

# Compute positions for the remaining nodes
dynamic_positions = nx.spring_layout(G, weight=custom_distance, pos=fixed_positions)

# Update positions dictionary with fixed positions
pos = {**fixed_positions, **dynamic_positions}

# Draw the graph with fixed positions for specified nodes
nx.draw(G, pos, with_labels=True, node_size=200, node_color="skyblue", font_size=8, font_weight="bold")
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Display the graph
plt.show()
