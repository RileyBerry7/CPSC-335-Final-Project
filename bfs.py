from collections import deque

def bfs(adj_list, start_point, end_point):
    visited = set()
    queue = deque([(start_point, [start_point])]) 

    while queue:
        current_node, path = queue.popleft()
        if current_node == end_point:
            print(path)
            return path
        if current_node not in visited:
            visited.add(current_node)
            for neighbor, _ in adj_list[current_node].items():
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    print("No path found from ", start_point, " to ", end_point)
    return None, None