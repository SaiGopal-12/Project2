import numpy as np
import cv2
from queue import PriorityQueue
import math as m
import time as tm


import numpy as np
import cv2

from utils import *
from backtracking import *

def move(current_positions, direction):
    directions = {
        'up': (0, 1),
        'down': (0, -1),
        'right': (1, 0),
        'left': (-1, 0),
        'up_right': (1, 1),
        'up_left': (-1, 1),
        'down_right': (1, -1),
        'down_left': (-1, -1),
    }

    new_pos = (current_positions[0] + directions[direction][0], current_positions[1] + directions[direction][1])
    
    if  direction=='up' or  direction =='down' or  direction=='left' or  direction=='right':
        cost = 1 # up, down, right, left cost
    else:
        cost = 1.4  # Diagonal movement cost
    return new_pos, cost

def feasible_appends(current_positions, map_data):
    return [
        [position, cost] 
        for position, cost in current_positions 
        if 0 <= position[1] < 500 and 0 <= position[0] < 1200 
        and (map_data[(499 - position[1]), position[0]] == [0, 0, 0]).all()
    ]
    
def find_neighbors(node, map_data):
    current_positions = [node.position[0], node.position[1]]
    
    directions = ['up', 'down', 'right', 'left', 'up_right', 'down_right', 'up_left', 'down_left']
    con_neigh_list = [move(current_positions.copy(), direction) for direction in directions]
    nxt_neigh = feasible_appends(con_neigh_list, map_data )
    return nxt_neigh