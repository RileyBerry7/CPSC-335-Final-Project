import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from parser import parse_csv
import matplotlib.image as mpimg

# Load data from CSV into the graph
graph = parse_csv('edgeinformation.csv')
image1 = mpimg.imread('campus map node graph.png')
# Create a undirected graph
G = nx.Graph()

# Add edges from the adjacency list
for node in graph:
    for neighbor, weight in graph[node]:
        if weight == 999:
            continue
        G.add_edge(node, neighbor, weight=weight)
        
node_positions = {
    #left border
    '1':(-1.134,1.119),
    '39' :(-1.134,0.836),
    '36':(-1.134,.655),
    '35':(-1.134,.474),
    '40':(-1.134,.293),
    '41':(-1.134,.102),
    '42':(-1.134,-.079),
    '91':(-1.134,-.26),
    '96':(-1.134,-.441),
    '97':(-1.134,-.622),
    '98':(-1.134,-.99),
    
    #top border
    
    '2':(-.72,1.17),
    '3':(-.38,1.169),
    '4':(-.094,1.167),
    '5':(0.268,1.053),
    '6':(0.583,0.997),
    
    #right border
    
    '7':(.7,.754),
    '8':(.7,.59),
    '12':(.66,0.37),
    '13':(.66,.218),
    '14':(.66,.038),
    '15':(.66,-.2),
    '16':(.582,-.342),
    '68':(.587,-.628),
    '69':(.587,-.739),
    '114':(.598,-.739),
    '113':(.603, -1.008),
    '112':(0.587,-1.13),
    
    #bottom border
    
    '111':(.476,-1.106),
    '110':(.34,-1.15),
    '100':(-.31,-1.13),
    '99':(-.69,-1.11),
    # Add positions for other nodes
}

spring_positions = nx.spring_layout(G, k=0.15, iterations=50)
pos = {**spring_positions, **node_positions}

# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.imshow(image1, extent = [0,1,0,1], alpha = .5)

# Display the graph
plt.show()
