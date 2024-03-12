import numpy as np
import cv2
from queue import PriorityQueue
import math as m
import time as tm
import cv2

def draw_rotated_hexagon(image, center, side_length, color, rotation_angle, thickness=1):
    # Calculate the coordinates of the hexagon vertices
    angle = 60  # Angle between consecutive vertices of a regular hexagon
    hexagon_points = np.array([
        [
            int(center[0] + side_length * np.cos(np.radians(i * angle + rotation_angle))),
            int(center[1] + side_length * np.sin(np.radians(i * angle + rotation_angle)))
        ]
        for i in range(6)
    ], np.int32)

    # Reshape the array to the required format
    hexagon_points = hexagon_points.reshape((-1, 1, 2))

    # Draw the filled hexagon
    cv2.fillPoly(image, [hexagon_points], color)

    # Draw the hexagon outline
    cv2.polylines(image, [hexagon_points], isClosed=True, color=(255, 255, 255), thickness=thickness)

side_length = 150
center = (600, 250)
rotation_angle = 90
image = np.zeros((500, 800, 3), dtype=np.uint8) 
draw_rotated_hexagon(image, center, side_length, (0, 255, 0), rotation_angle, thickness=2)

def generated_map():
    # Create a blank image
    arena = np.zeros((500, 1200, 3), dtype="uint8")
    
    # Draw the outer boundary
    cv2.rectangle(arena, (-1, -1), (1199, 499), (255, 255, 255), 10)

    # Draw filled rectangles
    cv2.rectangle(arena, (175, 0), (100, 400), (255, 0, 0), -1)
    cv2.rectangle(arena, (275, 500), (350, 100), (255, 0, 0), -1)

    # Draw rectangle outlines
    cv2.rectangle(arena, (175, 0), (100, 400), (255, 255, 255), 5)
    cv2.rectangle(arena, (275, 500), (350, 100), (255, 255, 255), 5)

    # Define the polygon points
    poly_points = np.array([[900, 50], [1100, 50], [1100, 450], [900, 450],
                            [900, 375], [1020, 375], [1020, 125], [900, 125]])

    # Draw a rotated hexagon
    draw_rotated_hexagon(arena, (600, 250), 150, (255, 0, 0), 90, 5)

    # Draw filled polygon
    cv2.fillPoly(arena, [poly_points], color=(255, 0, 0))

    # Draw polygon outline
    cv2.polylines(arena, [poly_points], isClosed=True, color=(255, 255, 255), thickness=5)

    return arena
generated_map()

def initialize_variables():
    global map_data, queue, visited_set, node_objects
    map_data = generated_map()
    queue = PriorityQueue()
    visited_set = set([])
    node_objects = {} 
    result_frames=[]
    return map_data, queue, visited_set, node_objects, result_frames

def check_valid_coordinates(coords):
    # Check if each coordinate is a valid integer
    if all(isinstance(coord, int) for coord in coords):
        # Add range checks based on the dimensions of your map
        x, y = coords
        if 0 <= x < map_width and 0 <= y < map_height:
            return True
        else:
            print("Coordinates out of range. Please enter valid coordinates.")
    else:
        print("Invalid coordinate format. Please enter integer coordinates.")
    
    return False

map_width = 1200
map_height = 500

def get_user_input():
    start_valid = False
    goal_valid = False

    while not (start_valid and goal_valid):
        try:
            start_input = input("Enter starting coordinates (x y): ").split()
            goal_input = input("Enter goal coordinates (x y): ").split()

            start_point = [int(coord) for coord in start_input]
            end_node = [int(coord) for coord in goal_input]

            if len(start_point) == len(end_node) == 2:
                start_valid = check_valid_coordinates(start_point)
                goal_valid = check_valid_coordinates(end_node)

            if not start_valid:
                print("Invalid starting coordinates. Please try again.")

            if not goal_valid:
                print("Invalid goal coordinates. Please try again.")

        except ValueError:
            print("Invalid input. Please enter integer coordinates.")

    return start_point, end_node