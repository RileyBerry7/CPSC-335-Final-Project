import numpy as np
import matplotlib.image as mpimg
import networkx as nx
import parser
import csv


def generate_traffic(ax, canvas, accessibility):
    # Clear existing graph
    ax.clear()

    # Load data from CSV into the graph
    graph = parser.parse_graph_csv('edgeinformation.csv')

    # Create an undirected graph
    G = nx.Graph()

    # Add edges from the adjacency list
    for node in graph:
        for neighbor, weight, color, wheelchair, incline in graph[node]:
            # Exclude edges with weight 999 or greater
            if weight >= 999:
                G.add_edge(node, neighbor, weight=weight, color='black')
            elif accessibility == 'Wheelchair Only' and wheelchair == "No":
                G.add_edge(node, neighbor, weight=1000, color='purple')
            elif accessibility == 'No Steep Inclines' and incline == "Yes":
                G.add_edge(node, neighbor, weight=1000, color='purple')
            else:
                # Apply traffic algorithm
                randNum = np.random.randint(1, 15)
                final_weight = weight * randNum / 3
                # Assign edge color based on the new weight
                edge_color = 'green' if 1 <= randNum <= 9 else \
                    'yellow' if 10 <= randNum <= 11 else \
                        'orange' if 12 <= randNum <= 13 else \
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
        if G[u][v]['weight'] == 1000:
            # Draw black edges with slightly larger width as outline
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color='black', width=3.5)
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color=G[u][v]['purple'], width=3.5)

    # Load and overlay the campus map image
    image = mpimg.imread('campus map node graph.png')
    image_width = 629
    image_height = 897
    ax.imshow(image, extent=[0, image_width, 0, image_height], alpha=1)
    ax.axis('off')

    # Update canvas
    canvas.draw()

    return G


def change_edges_color(G, pos, ax, canvas, nodes_to_color):
    edges = G.edges()
    for u, v in edges:
        if (u in nodes_to_color and v in nodes_to_color) or (v in nodes_to_color and u in nodes_to_color):
            # Draw edges between nodes in nodes_to_color array in purple
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color='purple', width=3.5)
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(v, u)], edge_color='purple', width=3.5)
        # else:
        #     nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color='black', width=3.5)

    canvas.draw()