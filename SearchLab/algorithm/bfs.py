from itertools import islice
from .common import Node, child_node, solution, Queue, enqueue, dequeue, is_empty


def BFS(problem, trace):
    node = Node(problem.initial_state)
    if problem.is_goal(node.state):
        trace.append((None, (), 0))
        return solution(node)
    frontier = Queue()
    enqueue(frontier, node)
    explored = set()
    queued = {node.state}
    trace.append((None, tuple(item.state for item in islice(frontier, 6)), len(frontier)))
    while not is_empty(frontier):
        node = dequeue(frontier)
        queued.remove(node.state)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in queued:
                if problem.is_goal(child.state):
                    trace.append((node.state, tuple(item.state for item in islice(frontier, 6)), len(frontier)))
                    return solution(child)
                queued.add(child.state)
                enqueue(frontier, child)
        trace.append((node.state, tuple(item.state for item in islice(frontier, 6)), len(frontier)))
    return None
