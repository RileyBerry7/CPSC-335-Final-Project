def dijkstra_algorithm(adjacency_list, origin, destination):

    distance = {node: float('infinity') for node in adjacency_list}
    previous = {node: None for node in adjacency_list}
    distance[origin] = 0

    priority_queue = [(0, origin)]

    while priority_queue:
        current_distance, current_node = min(priority_queue)
        priority_queue.remove((current_distance, current_node))

        if current_node == destination:
            path = []
            while previous[current_node]:
                path.append(current_node)
                current_node = previous[current_node]
            path.append(origin)
            path.reverse()
            distance[destination] -= (999*2)
            print(f"Shortest path: {path} and total distance: {distance[destination]}")
            return distance[destination], path

        for neighbor, edge_info in adjacency_list[current_node].items():
            weight = edge_info['weight']
            if weight == 999 and not (current_node == origin or neighbor == destination):
                continue
            new_distance = current_distance + weight

            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance
                previous[neighbor] = current_node
                priority_queue.append((new_distance, neighbor))

    print("No path found from ", origin, " to ", destination)
    return None, None
