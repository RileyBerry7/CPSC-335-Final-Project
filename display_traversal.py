import networkx as nx

def display_traversal(G, pos, node_list, ax):
    # Draw nodes
    nx.draw(G, pos, with_labels=False, node_size=0, node_color="black", font_size=8, font_weight="bold",
            ax=ax)

    # Draw edges between nodes in node_list as blue with slightly thicker width
    for i in range(len(node_list) - 1):
        u = node_list[i]
        v = node_list[i + 1]
        if G.has_edge(u, v):
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax, edge_color='blue', width=3.4)

    # Update canvas
    ax.figure.canvas.draw_idle()
