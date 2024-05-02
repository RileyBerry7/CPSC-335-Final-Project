from collections import deque

# def bfs(adj_list, start_point, end_point):
#     visited = set()
#     queue = deque([(start_point, 0, [start_point])])
#
#     while queue:
#         current_node, total_weight, path = queue.popleft()
#         if current_node == end_point:
#             #print(total_weight, path)
#             return total_weight, path
#         if current_node not in visited:
#             visited.add(current_node)
#             for neighbor, edge_info in adj_list[current_node].items():
#                 weight = edge_info['weight']
#                 new_total_weight = total_weight + weight
#                 new_path = path + [neighbor]
#                 queue.append((neighbor, new_total_weight, new_path))
#
#     print("No path found from ", start_point, " to ", end_point)
#     return None, None

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
           for neighbor in adj_list[current_node]:
               queue.append((neighbor, path + [neighbor]))


   print("No path found from ", start_point, " to ", end_point)
   return None