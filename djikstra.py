import numpy as np
from queue import PriorityQueue
import math as m
import time as tm
import cv2

from move_files import find_neighbors, move, feasible_appends
from utils import *

class Node:
    def __init__(self,position,cost,parent):
        self.position = position
        self.cost = cost
        self.parent = parent
    

def dijkstra_algorithm(map_data, queue, visited_set, node_objects, start_node, end_node,result_frames):
    node_cost = {str([i, j]): float('inf') for i in range(500) for j in range(1200)}
    node_cost[str(start_node)] = 0
    visited_set.add(str(start_node))
    current_node = Node(start_node, 0, None)
    node_objects[str(current_node.position)] = current_node
    queue.put([current_node.cost, current_node.position])
    iteration = 0

    while not queue.empty():
        current_queue_node = queue.get()
        current_node = node_objects[str(current_queue_node[1])]

        if current_queue_node[1][0] == end_node[0] and current_queue_node[1][1] == end_node[1]:
            node_objects[str(end_node)] = Node(end_node, current_queue_node[0], current_node)
            break

        for neighbor_node, neighbor_cost in find_neighbors(current_node, map_data):
            if str(neighbor_node) in visited_set:
                updated_neighbor_cost = neighbor_cost + node_cost[str(current_node.position)]
                if updated_neighbor_cost < node_cost[str(neighbor_node)]:
                    node_cost[str(neighbor_node)] = updated_neighbor_cost
                    node_objects[str(neighbor_node)].parent = current_node
            else:
                visited_set.add(str(neighbor_node))
                map_data[(499 - neighbor_node[1]), neighbor_node[0], :] = np.array([0, 255, 0])

                if iteration % 1000 == 0:
                    result_frames.append(map_data.copy())
                    cv2.imshow("AnimationVideo", map_data)
                    cv2.waitKey(1)

                updated_cost = neighbor_cost + node_cost[str(current_node.position)]
                node_cost[str(neighbor_node)] = updated_cost
                next_node = Node(neighbor_node, updated_cost, node_objects[str(current_node.position)])
                queue.put([updated_cost, next_node.position])
                node_objects[str(next_node.position)] = next_node

        iteration += 1

    return node_objects