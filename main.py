import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph
graph = {}

# Building out the adjacency list 1 node at a time ;-;
edges = [
    (1, 2, 220), (1, 39, 160),
    (2, 27, 141), (2, 3, 69),
    (3, 4, 113),
    (4, 5, 175), (4, 25, 78),
    (5, 25, 181),
    (25, 26, 60),
    (26, 27, 124)
]

# Populate adjacency list
for edge in edges:
    source, target, weight = edge
    if source not in graph:
        graph[source] = []
    graph[source].append((target, weight))

# Create a directed graph
G = nx.Graph()

# Add edges from the adjacency list
for node in graph:
    for neighbor, weight in graph[node]:
        G.add_edge(node, neighbor, weight=weight)

# Draw the graph
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Display the graph
plt.show()
