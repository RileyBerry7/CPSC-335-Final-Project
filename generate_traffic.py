import numpy as np
import matplotlib.image as mpimg
import networkx as nx
import parser

def generate_traffic(ax, canvas):
    # Clear existing graph
    ax.clear()

    # Load data from CSV into the graph
    graph = parser.parse_graph_csv('edgeinformation.csv')

    # Create an undirected graph
    G = nx.Graph()

    # Add edges from the adjacency list
    for node in graph:
        for neighbor, weight in graph[node]:
            # Exclude edges with weight 999 or greater
            if weight >= 999:
                G.add_edge(node, neighbor, weight=weight, color='black')
            else:
                # Apply traffic algorithm
                randNum = np.random.randint(1, 15)
                final_weight = weight * randNum / 3
                # Assign edge color based on the new weight
                edge_color = 'green' if 1 <= randNum <= 9 else \
                             'yellow' if 10 <= randNum <= 12 else \
                             'orange' if 13 <= randNum <= 14 else \
                             'red'
                # Add edge with updated weight
                G.add_edge(node, neighbor, weight=final_weight, color=edge_color)

    # Call the parser function to read the node position CSV file
    node_positions = parser.parse_node_positions_csv("nodepositions.csv")
    pos = node_positions

    # Draw nodes *Black Edges too
    nx.draw(G, pos, with_labels=False, node_size=0, node_color="black", font_size=8, font_weight="bold",
            ax=ax, width=0)

    # Draw edges with updated colors and black outline
    edges = G.edges()
    for u, v in edges:
        if G[u][v]['weight'] < 999:
            # Draw black edges with slightly larger width as outline
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color='black', width=3.5)
            # Draw colored edges with desired width
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color=G[u][v]['color'], width=3.3)

    # Load and overlay the campus map image
    image = mpimg.imread('campus map node graph.png')
    image_width = 629
    image_height = 897
    ax.imshow(image, extent=[0, image_width, 0, image_height], alpha=1)
    ax.axis('off')

    # Update canvas
    canvas.draw()
