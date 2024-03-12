import numpy as np
from queue import PriorityQueue
import math as m
import time as tm
import cv2

from move_files import *
from djikstra import *
from backtracking import *
from utils import *

def main():
        map_data, queue, visited_set, node_objects, result_frames=initialize_variables()
        start_point, end_node= get_user_input()
        start_t = tm.time()
        node_objects=dijkstra_algorithm(map_data,queue,visited_set, node_objects,start_point, end_node, result_frames)
        back_track_list=backtracking(node_objects=node_objects, end_node=end_node)
        end_time = tm.time()
        
        for value in back_track_list:
            map_data[value[0], value[1], :] = np.array([255, 0, 0])
            result_frames.append(map_data.copy())
            cv2.imshow("AnimationVideo", map_data)
            cv2.waitKey(1)

        print("Quickest path which is optimal path: {:.2f}".format(end_time - start_t), " seconds")

    
        video = cv2.VideoWriter(
            'AnimationVideo.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 25, (1200, 500))

        for i in range(len(result_frames)):
            frame = result_frames[i]
            video.write(frame)
        video.release()

        print("video stored at directory path")      
if __name__ =="__main__":
    main()