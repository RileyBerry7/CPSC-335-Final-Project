import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from parser import parse_csv

# Load data from CSV into the graph
graph = parse_csv('edgeinformation.csv')

# Create a undirected graph
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
