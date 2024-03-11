import numpy as np
from queue import PriorityQueue
import math as m
import time as tm


import numpy as np
import cv2

from move_files import *
from djikstra import *
from backtracking import *
from utils import *


def main():
        map, que, visSet, nodeObj, video_Stream=initialize_variables()
        strtNode, goalNode= get_user_input()
        start_t = tm.time()
        nodeObj=dijkstra_algorithm(map=map,que=que,visSet=visSet, nodeObj=nodeObj, video_Stream=video_Stream, strtNode=strtNode, goalNode=goalNode)
        back_track_list=backtracking(nodeObj=nodeObj, goalNode=goalNode)
        end_time = tm.time()
        
        for value in back_track_list:
            map[value[0], value[1], :] = np.array([255, 0, 0])
            video_Stream.append(map.copy())
            cv2.imshow("Dijkstra Algorithm", map)
            cv2.waitKey(1)

        print("Quickest path which is optimal path: {:.2f}".format(end_time - start_t), " seconds")

    
        video = cv2.VideoWriter(
            'dijkstra.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 25, (1200, 500))

        for i in range(len(video_Stream)):
            frame = video_Stream[i]
            video.write(frame)
        video.release()

        print("video stored at directory path")      
if __name__ =="__main__":
    main()