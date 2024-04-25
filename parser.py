import csv

def parse_csv(filename):
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
