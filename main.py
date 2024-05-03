import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import parser
from generate_traffic import generate_traffic
from generate_traffic import change_edges_color
import matplotlib.image as mpimg
import bfs
import dfs
import dijkstra

class CampusNavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Navigation System")
        self.root.geometry("1200x600")
        self.root.configure(bg="#1e1e1e")  # Set background color to dark gray

        # Dark mode styling for the top bar
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a classic theme for consistent appearance across platforms
        self.style.configure('.', background='#1e1e1e', foreground='white')  # Set default foreground and background
        self.style.configure('TButton', background='#333', font=('Helvetica', 12))  # Dark mode button style
        self.style.configure('TFrame', background='#1e1e1e')  # Dark mode frame background
        self.style.configure('TCombobox', foreground='black')  # Set dropdown text color to black

        graph = parser.parse_graph_csv('edgeinformation.csv')

        # Create an undirected graph
        self.G = nx.Graph()

        # Add edges from the adjacency list
        for node in graph:
            for neighbor, weight, color, wheelchair, incline in graph[node]:
                self.G.add_edge(node, neighbor, weight=weight, color=color)


        # Create UI elements
        self.create_input_panel()
        self.create_canvas()
        self.canvas_update_interval = 10  # Update canvas every 100 milliseconds

    def create_input_panel(self):
        self.input_panel = ttk.Frame(self.root, padding="20")
        self.input_panel.grid(row=0, column=0, sticky="ns")

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

        # Accessibility Selection
        ttk.Label(self.input_panel, text="Accessibility:").grid(row=3, column=0, stick="w")
        self.accessibility_combo = ttk.Combobox(self.input_panel, width=20, state="readonly")
        self.accessibility_combo["values"] = ["None", "Wheelchair Only", "No Steep Inclines"]
        self.accessibility_combo.grid(row=3, column=1)

        # Button to execute the selected algorithm
        self.execute_button = ttk.Button(self.input_panel, text="Execute", command=self.execute_algorithm)
        self.execute_button.grid(row=200, column=0, columnspan=2, pady=20, sticky="ew")  # Centered in the left panel side

        # Generate traffic button
        self.traffic_button = ttk.Button(self.input_panel, text="Generate traffic", command=self.generate_traffic)
        self.traffic_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Distance textbox
        self.distance_text = ttk.Label(self.input_panel, text="Distance: ")
        self.distance_text.grid(row=500, column=0, pady=10, sticky="ew")
        
        # Time textbox
        self.time_text = ttk.Label(self.input_panel, text = "Time: ")
        self.time_text.grid(row=600, column=0, pady=10, sticky="ew")
        
        # Clear button
        self.clear_button = ttk.Button(self.input_panel, text="Clear", command = self.reset_canvas)
        self.clear_button.grid(row=1000, column = 0, columnspan = 2, pady = 10, sticky= "ew")
    
    #Clear button function
    def reset_canvas(self):
        self.G.clear()  
        graph = parser.parse_graph_csv('edgeinformation.csv')
        for node in graph:
            for neighbor, weight, color, wheelchair, incline in graph[node]:
                self.G.add_edge(node, neighbor, weight=weight, color="black")

        #Reset distance and time textboxes
        self.start_combo.set('')
        self.end_combo.set('')
        self.algorithm_combo.set('')
        self.distance_text.config(text="Distance:  mi")
        self.time_text.config(text="Time:  min")

        self.ax.cla()  
        self.create_canvas()  
        
    def generate_traffic(self):
        accessibility = self.accessibility_combo.get()
        self.G = generate_traffic(self.ax, self.canvas, accessibility)

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
            for neighbor, weight, color, wheelchair, incline in graph[node]:
                if weight < 999:  # Only add edges with weight less than 999
                    G.add_edge(node, neighbor, weight=weight)

        # call the parser function to read the node position CSV file
        node_positions = parser.parse_node_positions_csv("nodepositions.csv")
        pos = node_positions

        self.fig, self.ax = plt.subplots(figsize=(6, 6))

        # Draw nodes
        nx.draw(G, pos, with_labels=False, node_size=0, node_color="black", font_size=8, font_weight="bold",
                ax=self.ax)

        # Draw edges with width based on weight
        for u, v, d in G.edges(data=True):
            if d['weight'] < 999:
                # orgiginal black line width
                nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=self.ax, width=3.5)

        image_width = 629
        image_height = 897

        # alpha here controls transparency of backround image (0 - 1)
        self.ax.imshow(image, extent=[0, image_width, 0, image_height], alpha=1)
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
    def execute_algorithm(self):
        graph = parser.parse_graph_csv('edgeinformation.csv')
        node_positions = parser.parse_node_positions_csv("nodepositions.csv")

        G = nx.Graph()

        # Add edges from the adjacency list
        for node in graph:
            for neighbor, weight, color, wheelchair, incline in graph[node]:
                if weight >= 999:
                    randNum = np.random.randint(8, 15)
                    final_weight = weight/randNum
                    G.add_edge(node, neighbor, weight=final_weight)
                else:
                    G.add_edge(node, neighbor, weight=weight)

        pos = node_positions

        start_point = self.start_combo.get()
        end_point = self.end_combo.get()
        algorithm = self.algorithm_combo.get()

        if algorithm == 'BFS':
            weight, path = bfs.bfs(G.adj,start_point,end_point)
            change_edges_color(G, pos, self.ax, self.canvas, path)
        elif algorithm == 'DFS':
            weight, path = dfs.dfs(G.adj,start_point,end_point)
            change_edges_color(G, pos, self.ax, self.canvas, path)
        elif algorithm == "Dijkstra's":
            weight, path = dijkstra.dijkstra_algorithm(self.G.adj,start_point,end_point)
            change_edges_color(G, pos, self.ax, self.canvas, path)
        
        distance_in_mile = weight * 0.000621371
        if distance_in_mile < .1:
            rounded_distance = round(distance_in_mile,6)
        else:
            rounded_distance = round(distance_in_mile,2)
        time = round(distance_in_mile/3*60)
        print(time)
        self.distance_text.config(text="Distance: " + str(rounded_distance) + " miles")
        self.time_text.config(text="Time: " + str(time) + " minutes")



if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationApp(root)
    root.mainloop()
