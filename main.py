import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

import parser


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
        # Implement traffic generation functionality here
        pass

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

        node_positions = {
            'A Parking': (106.715, 754.148),
            'G Parking': (253.278, 843.199),
            'Fullerton Arboretum': (482.398, 719.826),
            'Goodwin Field': (333.980, 702.202),
            'Titan Stadium': (253.278, 704.984),
            'Anderson Field': (333.052, 667.880),
            'Titan Sports Complex': (332.125, 629.848),
            'Soccer Field': (257.916, 598.309),
            'Tennis Courts': (238.436, 521.317),
            'Intramural Area': (329.342, 523.173),
            'Children\'s Center': (154.412, 635.765),
            'A-South Parking': (126.322, 594.567),
            'Parking & Transport Office': (63.588, 615.166),
            'Corporation Yard': (94.487, 523.406),
            'D Parking': (160.030, 513.106),
            'Titan House': (404.411, 480.335),
            'Ruby Gerontology Center': (469.017, 458.800),
            'Residence Halls': (565.459, 648.874),
            'Housing Office': (525.197, 580.522),
            'Student Housing': (537.369, 489.698),
            'Student Health & Counseling Center': (409.092, 411.983),
            'Titan Gymnasium': (279.879, 411.983),
            'Student Rec Center': (185.310, 414.792),
            'State College Parking Structure': (115.086, 409.174),
            'University Police': (58.906, 408.238),
            'Golleher Alumni House': (58.906, 338.950),
            'Titan Student Union': (140.367, 311.796),
            'Bookstore/Titan Shops': (213.400, 318.351),
            'Pollak Library': (320.141, 295.879),
            'Education-Classroom': (393.175, 279.961),
            'Engineering': (459.654, 352.995),
            'Computer Science': (505.534, 352.995),
            'E Parking': (558.904, 307.115),
            'I Parking': (474.635, 281.834),
            'Becker Ampitheatre': (171.266, 263.108),
            'Visual Arts': (131.940, 237.827),
            'Clayes Performing Arts Center': (233.999, 211.610),
            'Quad': (330.441, 205.992),
            'Humanities-Social Science': (403.474, 205.055),
            'F Parking': (480.253, 191.947),
            'Eastside Parking Structure': (561.713, 226.591),
            'University Hall': (393.175, 147.003),
            'McCarthy Hall': (303.287, 142.322),
            'Greenhouse Complex': (240.554, 136.704),
            'Nutwood Parking Structure': (128.195, 94.569),
            'Dan Black Hall': (292.052, 100.187),
            'Carl\'s Jr.': (419.392, 119.850),
            'Langsdorf Hall': (381.003, 83.333),
            'Mihaylo Hall': (452.163, 73.033),
            'C Parking': (140.367, 46.816),
            'Fullerton Marriott': (582.313, 67.415),
            '1': (42.053, 869.847),
            '2': (202.164, 874.528),
            '3': (254.599, 875.465),
            '4': (334.186, 875.465),
            '5': (454.972, 833.330),
            '6': (581.376, 810.858),
            '7': (612.275, 721.907),
            '8': (608.530, 670.409),
            '9': (561.713, 668.537),
            '10': (502.725, 650.746),
            '11': (502.725, 584.267),
            '12': (578.567, 611.421),
            '13': (578.567, 555.241),
            '14': (577.631, 506.552),
            '15': (576.695, 418.538),
            '16': (519.579, 397.002),
            '17': (483.062, 398.875),
            '18': (493.362, 459.736),
            '19': (493.362, 504.680),
            '20': (439.991, 509.361),
            '21': (395.984, 510.297),
            '22': (395.984, 586.140),
            '23': (395.984, 683.518),
            '24': (376.321, 774.341),
            '25': (322.950, 820.221),
            '26': (297.670, 783.705),
            '27': (210.591, 768.723),
            '28': (195.610, 709.735),
            '29': (193.737, 657.301),
            '30': (196.546, 632.020),
            '31': (255.535, 632.020),
            '32': (185.310, 558.986),
            '33': (144.112, 560.859),
            '34': (95.423, 559.923),
            '35': (42.053, 557.114),
            '36': (41.116, 651.683),
            '37': (84.187, 653.555),
            '38': (132.876, 654.492),
            '39': (43.925, 754.678),
            '40': (39.244, 511.234),
            '41': (40.180, 453.182),
            '42': (41.116, 366.103),
            '43': (79.506, 365.167),
            '44': (89.805, 339.886),
            '45': (143.176, 351.122),
            '46': (147.857, 403.556),
            '47': (79.506, 403.556),
            '48': (83.251, 451.309),
            '49': (144.112, 449.436),
            '50': (191.865, 459.736),
            '51': (188.119, 513.106),
            '52': (240.554, 449.436),
            '53': (351.040, 448.500),
            '54': (400.665, 446.627),
            '55': (435.309, 443.818),
            '56': (439.991, 389.511),
            '57': (406.283, 384.830),
            '58': (362.276, 384.830),
            '59': (357.594, 414.792),
            '60': (353.849, 355.804),
            '61': (356.658, 316.478),
            '62': (371.639, 316.478),
            '63': (401.602, 315.542),
            '64': (426.882, 309.924),
            '65': (460.590, 308.987),
            '66': (478.380, 308.051),
            '67': (499.916, 310.860),
            '68': (524.260, 307.115),
            '69': (519.579, 257.490),
            '70': (452.163, 257.490),
            '71': (436.246, 254.681),
            '72': (398.793, 248.126),
            '73': (345.422, 249.999),
            '74': (320.141, 249.063),
            '75': (294.861, 249.063),
            '76': (346.358, 299.624),
            '77': (299.542, 288.388),
            '78': (297.670, 359.549),
            '79': (266.771, 355.804),
            '80': (267.707, 291.197),
            '81': (238.681, 296.815),
            '82': (239.617, 356.740),
            '83': (181.565, 375.467),
            '84': (193.737, 343.632),
            '85': (190.928, 299.624),
            '86': (230.254, 283.707),
            '87': (193.737, 250.935),
            '88': (131.940, 278.089),
            '89': (86.060, 279.961),
            '90': (42.053, 277.152),
            '91': (42.989, 232.209),
            '92': (96.360, 247.190),
            '93': (156.284, 254.681),
            '94': (152.539, 197.565),
            '95': (116.959, 153.557),
            '96': (41.116, 153.557),
            '97': (42.053, 100.187),
            '98': (46.734, 33.708),
            '99': (140.367, 28.090),
            '100': (219.018, 30.899),
            '101': (202.164, 63.670),
            '102': (191.865, 117.041),
            '103': (189.056, 168.539),
            '104': (247.108, 164.793),
            '105': (228.381, 119.850),
            '106': (241.490, 70.224),
            '107': (292.988, 69.288),
            '108': (351.976, 70.224),
            '109': (409.092, 66.479),
            '110': (415.647, 29.962),
            '111': (485.871, 49.625),
            '112': (525.197, 46.816),
            '113': (520.515, 111.423),
            '114': (522.388, 129.213),
            '115': (496.171, 116.104),
            '116': (473.699, 123.595),
            '117': (437.182, 100.187),
            '118': (429.691, 132.022),
            '119': (403.474, 132.022),
            '120': (403.474, 101.123),
            '121': (353.849, 100.187),
            '122': (359.467, 126.404),
            '123': (266.771, 114.232),
            '124': (292.052, 165.730),
            '125': (318.269, 168.539),
            '126': (354.785, 163.857),
            '127': (376.321, 176.029),
            '128': (373.512, 207.864),
            '129': (429.691, 174.157),
        }
        pos = node_positions

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        nx.draw(G, pos, with_labels=False, node_size=50, node_color="skyblue", font_size=8, font_weight="bold",
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
        start_point = self.start_combo.get()
        end_point = self.end_combo.get()
        algorithm = self.algorithm_combo.get()

        # Execute selected algorithm and update graph display accordingly
        # Add your algorithm implementation here


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationApp(root)
    root.mainloop()
