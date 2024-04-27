import csv

def parse_graph_csv(filename):
    graph = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            edge_relation = row['Edge Relation']
            edge_weight_str = row['Edge Weight']
            try:
                edge_weight = int(edge_weight_str)
            except ValueError:
                print(f"Skipping row with invalid weight: {row}")
                continue
            source, dest = edge_relation.split(' to ')
            if source not in graph:
                graph[source] = []
            graph[source].append((dest, edge_weight))
    return graph

def parse_location_csv(filename):
    locations = []
    with open(filename) as r:
        reader = csv.DictReader(r)
        for row in reader:
            if not row['Locations'].__contains__("Stop"):
                locations.append(row['Locations'])

    return locations
