import numpy as np
import cv2
from queue import PriorityQueue
import math as m
import time as tm


import numpy as np
import cv2


def draw_rotated_hexagon(image, center, side_length, color, rotation_angle, thickness=1):
    """
    Draw a rotated hexagon on the given image.

    Parameters:
    - image: The image on which to draw the hexagon.
    - center: The center coordinates of the hexagon.
    - side_length: The length of each side of the hexagon.
    - color: The color of the hexagon.
    - rotation_angle: The rotation angle of the hexagon in degrees.
    - thickness: (Optional) The thickness of the hexagon outline (default is 1).
    """
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

# Example usage:
side_length = 150
center = (600, 250)
rotation_angle = 90
image = np.zeros((500, 800, 3), dtype=np.uint8)  # Example blank image
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
# generated_map()

def initialize_variables():
    global map, que, visSet, nodeObj
    map = generated_map()
    que = PriorityQueue()
    visSet = set([])
    nodeObj = {} 
    video_Stream=[]
    return map, que, visSet, nodeObj, video_Stream

def check_coordinate(map, start_point, end_point):
    # Check if the start point is on border or inside obstacle
    condition_to_start = (map[(499 - start_point[1]), end_point[0]] == [0, 0, 0]).all()
    
    # Check if the end point is on border, inside obstacle, or okay
    condition_to_end = (map[(499 - end_point[1]), end_point[0]] == [0, 0, 0]).all() if condition_to_start else False
    
    if not condition_to_start:
        print("The start coordinate is", "on border" if (map[(499 - start_point[1]), start_point[0]] == [255, 255, 255]).all() else "inside obstacle")
        return False

    if not condition_to_end:
        print("The goal coordinate is", "on border" if (map[(499 - end_point[1]), end_point[0]] == [255, 255, 255]).all() else "inside obstacle")
        return False

    print("Started")
    return True

def get_user_input():
    # global strtNode, goalNode
    status = False
    while not status:
        strtNode = [int(ele) for ele in input("Enter starting coordinates: ").split(" ")]
        goalNode = [int(ele) for ele in input("Enter goal coordinates: ").split(" ")]
        status = check_coordinate(map, strtNode, goalNode)
    return strtNode, goalNode