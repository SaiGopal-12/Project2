def backtracking(node_objects, end_node):
    final_node = node_objects[str(end_node)]
    current_node = final_node.parent
    path_list = []

    while current_node:
        path_list.append([(499 - current_node.position[1]), current_node.position[0]])
        current_node = current_node.parent

    path_list.reverse()
    return path_list