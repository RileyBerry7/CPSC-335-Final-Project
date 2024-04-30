import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import parser
from generate_traffic import generate_traffic
import matplotlib.image as mpimg
import bfs

class CampusNavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Navigation System")
        self.root.geometry("1200x600")

        # Create UI elements
        self.create_input_panel()
        self.create_canvas()
        self.canvas_update_interval = 10  # Update canvas every 100 milliseconds

    def create_input_panel(self):
        self.input_panel = ttk.Frame(self.root, padding="20", style="Dark.TFrame")
        self.input_panel.grid(row=0, column=0, sticky="ns")
        self.input_panel.configure(style="InputPanel.TFrame")

        locations = parser.parse_location_csv('locations.csv')

        # Start point
        ttk.Label(self.input_panel, text="Start Point:").grid(row=0, column=0, sticky="w")
        self.start_combo = ttk.Combobox(self.input_panel, width=20, state="readonly")
        self.start_combo["values"] = locations  # Add your campus locations here
        self.start_combo.grid(row=0, column=1)

        # End point
        ttk.Label(self.input_panel, text="End Point:").grid(row=1, column=0, sticky="w")
        self.end_combo = ttk.Combobox(self.input_panel, width=20, state="readonly")
        self.end_combo["values"] = locations  # Add your campus locations here
        self.end_combo.grid(row=1, column=1)

        # Algorithm selection
        ttk.Label(self.input_panel, text="Algorithm:").grid(row=2, column=0, sticky="w")
        self.algorithm_combo = ttk.Combobox(self.input_panel, width=20, state="readonly")
        self.algorithm_combo["values"] = ["DFS", "BFS", "Dijkstra's"]  # Add more algorithms if needed
        self.algorithm_combo.grid(row=2, column=1)

        # Button to execute the selected algorithm
        self.execute_button = ttk.Button(self.input_panel, text="Execute", command=self.execute_algorithm,
                                         style="Accent.TButton")
        self.execute_button.grid(row=200, column=0, columnspan=2, pady=20,
                                 sticky="ew")  # Centered in the left panel side

        # Generate traffic button
        self.traffic_button = ttk.Button(self.input_panel, text="Generate traffic", command=self.generate_traffic,
                                         style="Accent.TButton")
        self.traffic_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Configure button style
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12))
        self.style.configure("InputPanel.TFrame", background="#f0f0f0")

    def generate_traffic(self):
        generate_traffic(self.ax, self.canvas)

    def create_canvas(self):
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")

        # Load data from CSV into the graph
        graph = parser.parse_graph_csv('edgeinformation.csv')
        image = mpimg.imread('campus map node graph.png')

        # Create an undirected graph
        G = nx.Graph()

        # Add edges from the adjacency list
        for node in graph:
            for neighbor, weight in graph[node]:
                G.add_edge(node, neighbor, weight=weight)

        # call the parser function to read the node position CSV file
        node_positions = parser.parse_node_positions_csv("nodepositions.csv")
        pos = node_positions

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        nx.draw(G, pos, with_labels=False, node_size=15, node_color="black", font_size=8, font_weight="bold",
                ax=self.ax, edge_color="gray", width=0.5)

        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='black', width=0.5)

        image_width = 629
        image_height = 897

        self.ax.imshow(image, extent=[0, image_width, 0, image_height], alpha=0.5)
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def execute_algorithm(self):
        graph = parser.parse_graph_csv('edgeinformation.csv')

        # Create an undirected graph
        G = nx.Graph()

        # Add edges from the adjacency list
        for node in graph:
            for neighbor, weight in graph[node]:
                G.add_edge(node, neighbor, weight=weight)
        start_point = self.start_combo.get()
        end_point = self.end_combo.get()
        algorithm = self.algorithm_combo.get()
        
        if algorithm == 'BFS':
            bfs.bfs(G.adj,start_point,end_point)

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationApp(root)
    root.mainloop()
