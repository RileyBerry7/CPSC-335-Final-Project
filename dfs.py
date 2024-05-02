from collections import deque

def dfs(adj_list, start_point, end_point):
    visited = set()
    stack = [(start_point, 0, [start_point])]

    while stack:
        current_node, total_weight, path = stack.pop()
        if current_node == end_point:
            print(total_weight, path)
            return total_weight, path
        if current_node not in visited:
            visited.add(current_node)
            for neighbor, edge_info in adj_list[current_node].items():
                weight = edge_info['weight']
                new_total_weight = total_weight + weight
                new_path = path + [neighbor]
                stack.append((neighbor, new_total_weight, new_path))

    print("No path found from ", start_point, " to ", end_point)
    return None, None
