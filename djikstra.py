import numpy as np
from queue import PriorityQueue
import math as m
import time as tm


import numpy as np
import cv2

from move_files import eig_Neigh, move, feasible_appends
from utils import *
class Node:
    def __init__(self,position,cost,parent):
        self.position = position
        self.cost = cost
        self.parent = parent
    


def dijkstra_algorithm(map, que, visSet, nodeObj, strtNode, goalNode,video_Stream):
    # global cost, nodeObj, que, visSet
    cost = {str([i, j]): m.inf for i in range(500) for j in range(1200)}
    cost[str(strtNode)] = 0
    visSet.add(str(strtNode))
    node = Node(strtNode, 0, None)
    nodeObj[str(node.position)] = node
    que.put([node.cost, node.position])
    iter = 0
    while not que.empty():
        queNode = que.get()
        node = nodeObj[str(queNode[1])]
        if queNode[1][0] == goalNode[0] and queNode[1][1] == goalNode[1]:
            nodeObj[str(goalNode)] = Node(goalNode, queNode[0], node)
            break

        for neighNode, neighCost in eig_Neigh(node, map):
            if str(neighNode) in visSet:
                neighUpdCost = neighCost + cost[str(node.position)]
                if neighUpdCost < cost[str(neighNode)]:
                    cost[str(neighNode)] = neighUpdCost
                    nodeObj[str(neighNode)].parent = node
            else:
                visSet.add(str(neighNode))
                map[(499 - neighNode[1]), neighNode[0], :] = np.array([0, 255, 0])
                
                if iter%1000 == 0:
                    video_Stream.append(map.copy())
                    cv2.imshow("Dijkstra Algorithm", map)
                    cv2.waitKey(1)
                
                updCost = neighCost + cost[str(node.position)]
                cost[str(neighNode)] = updCost
                nxtNode = Node(neighNode, updCost, nodeObj[str(node.position)])
                que.put([updCost, nxtNode.position])
                nodeObj[str(nxtNode.position)] = nxtNode           
        iter+=1
    return nodeObj