

def backtracking(nodeObj, goalNode):
    # global back_track_list
    back_track_node = nodeObj[str(goalNode)]
    Nodes = back_track_node.parent
    back_track_list = []

    while Nodes:
        back_track_list.append([(499 - Nodes.position[1]), Nodes.position[0]])
        Nodes = Nodes.parent

    back_track_list.reverse()   
    return back_track_list 