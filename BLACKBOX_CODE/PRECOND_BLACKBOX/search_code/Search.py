from constants import *
import signal
import copy
import time
from queue import Queue

def closed_list_key(node):
    return str(sorted(node[0]))


def BreadthFirstSearch(start_state, succ_generator, goal_test):
    fringe = Queue()
    closed = set()
    fringe.put(start_state)
    start_time = time.time()
    while not fringe.empty():
        node = fringe.get()  # [1]
        if goal_test(node):
            return node
        #print ("node", node[0])
        if closed_list_key(node) not in closed:
            closed.add(closed_list_key(node))
            successor_list = succ_generator(node)
            while successor_list:
                candidate_node = successor_list.pop()
                fringe.put(candidate_node)
    return None


